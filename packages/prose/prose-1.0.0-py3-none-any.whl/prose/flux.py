import numpy as np
import xarray as xr
from tqdm import tqdm
import matplotlib.pyplot as plt

from . import utils, models


def nu(n, sw, sr):
    return (sw ** 2) / n + sr ** 2


def pont2006(x, y, n=30, plot=True):
    dt = np.median(np.diff(x))
    ns = np.arange(1, n)
    binned = [utils.fast_binning(x, y, dt * _n)[1] for _n in ns]
    _nu = [np.var(b) for b in binned]
    X = np.hstack([(1/ns)[:, None], np.ones_like(ns)[:, None]])
    sw, sr = np.nan_to_num(np.sqrt(np.linalg.lstsq(X, _nu, rcond=None)[0]))
    if plot:
        plt.plot(ns, np.std(y) / np.sqrt(ns), ":k", label=r"$\sigma / \sqrt{n}$")
        plt.plot(ns, np.sqrt(nu(ns, sw, sr)), "k", label="fit")
        plt.plot(ns, np.sqrt(_nu), "d", markerfacecolor="w", markeredgecolor="k")
        plt.xlabel("n points")
        plt.ylabel("$\\nu^{1/2}(n)$")
        plt.legend()

    return sw, sr


def scargle(time, flux, error, X, n=1, plot=False, pmin=0.1, pmax=10., show_progress=True):
    def variability(p):
        return models.harmonics(time, p, n)

    def progress(x):
        return tqdm(x) if show_progress else x

    chi2 = []
    periods = np.linspace(pmin, pmax, 3000)
    kept_periods = []

    for p in progress(periods):
        try:
            x = models.design_matrix([X, *variability(p)])
            residuals = x @ np.linalg.lstsq(x, flux, rcond=None)[0] - flux
            _chi2 = np.sum((residuals / error) ** 2)
            if _chi2 > 1e10:
                continue
        except np.linalg.LinAlgError:
            continue

        chi2.append(_chi2)
        kept_periods.append(p)

    periods = np.array(kept_periods)
    period = periods[np.argmin(chi2)]

    # cleaning
    chi2 = np.array(chi2)
    chi2 = np.max(chi2) - chi2
    chi2 /= np.max(chi2)

    if plot:
        var = variability(period)
        x = models.design_matrix([X, *var])
        w = np.linalg.lstsq(x, flux, rcond=None)[0]
        corrected_flux = flux - x.T[0:-len(var)].T @ w.T[0:-len(var)].T

        plt.figure(figsize=(12, 4))
        plt.subplot(121)
        plt.xlabel("period")
        plt.axvline(period, c="0.9", lw=4)
        plt.plot(periods, chi2, c="k")

        plt.subplot(122)
        ft = (time + 0.5 * period) % period - 0.5 * period
        i = np.argsort(ft)

        variability = models.harmonics(ft[i], period, n)

        plt.plot(ft, corrected_flux, ".", c="0.7")
        x = np.hstack(variability)
        w = np.linalg.lstsq(x, corrected_flux[i], rcond=None)[0]
        plt.plot(ft[i], x @ w, "k")

    return period


class Flux:

    def __init__(self, xarray_or_flux, time=None, error=None, syst=None):
        if isinstance(xarray_or_flux, str):
            self.x = xr.load_dataset(xarray_or_flux)
        elif isinstance(xarray_or_flux, xr.Dataset):
            self.x = xarray_or_flux
        elif isinstance(xarray_or_flux, np.ndarray):
            self.x = xr.Dataset(dict(flux=xr.DataArray(xarray_or_flux, dims="time")), coords=dict(time=time))
            if error is not None:
                self.x['error'] = xr.DataArray(error, dims="time")
            if syst is not None:
                for name, data in syst.items():
                    self.x[name] = xr.DataArray(data, dims="time")

    def __copy__(self):
        return self.__class__(self.x.copy())

    def copy(self):
        return self.__copy__()

    def __getattr__(self, name):
        if name in self.x:
            return self.x[name].values
        elif name in self.x.attrs:
            return self.x.attrs[name]
        else:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute {name}")

    def _repr_html_(self):
        return self.x._repr_html_()

    def __iter__(self):
        return self.x.__iter__()

    def mask(self, mask, dim="time"):
        new_self = self.copy()
        new_self.x = new_self.x.where(xr.DataArray(mask, dims=dim), drop=True)
        return new_self

    @staticmethod
    def _binn(var, *bins):
        if var.dtype.name != 'object':
            if "time" in var.dims:
                if "error" in var.name:
                    return xr.concat(
                        [(np.sqrt(np.power(var.isel(time=b), 2).sum(dim="time")) / len(b)).expand_dims('time', -1) for b
                         in bins], dim="time")
                else:
                    return xr.concat([var.isel(time=b).mean(dim="time").expand_dims('time', -1) for b in bins],
                                     dim="time")
            else:
                return var
        else:
            return xr.DataArray(np.ones(len(bins)) * -1, dims="time")

    def binn(self, dt, std=False):
        x = self.x.copy()
        bins = utils.index_binning(self.time, dt)
        new_time = np.array([self.time[b].mean() for b in bins])

        x = x.map(self._binn, args=(bins), keep_attrs=True)

        if std:
            flu = self.x.flux.copy()
            x['error'] = xr.concat(
                [(flu.isel(time=b).std(dim="time") / np.sqrt(len(b))).expand_dims('time', -1) for b in bins],
                dim="time")

        x.coords['time'] = new_time

        return self.__class__(x)

    # io
    # ==

    @staticmethod
    def load(filepath):
        return Flux(xr.load_dataset(filepath))

    def save(self, filepath):
        self.x.to_netcdf(filepath)

    # plotting
    # ========

    def plot(self, which="None", bins=0.005, color="k", std=True):
        binned = self.binn(bins, std=std)
        plt.plot(self.time, self.flux, ".", c="gainsboro", zorder=0, alpha=0.6)
        plt.errorbar(binned.time, binned.flux, yerr=binned.error, fmt=".", zorder=1, color=color, alpha=0.8)

    def sigma_clip(self, sigma=3.):
        new_self = self.copy()
        new_self.xarray = new_self.xarray.sel(
            time=self.time[self.flux - np.median(self.flux) < sigma * np.std(self.flux)])
        return new_self

    # processing
    # ==========

    def where(self, condition):
        new_self = self.copy()
        new_self.x = new_self.x.sel(time=self.time[condition])
        return new_self

    def pont2006(self, plot=True):
        return pont2006(self.time, self.flux, plot=plot)

    def periodogram(self, X=None, n=1, plot=True, pmin=None, pmax=None, progress=True):
        if X is None:
            X = self.constant()
        return scargle(self.time, self.flux, self.error, X, n=n, plot=plot, pmin=pmin, pmax=pmax, show_progress=progress)

    def detrend(self, X):
        new_self = self.copy()
        new_self.x["flux"] = xr.DataArray(self.flux - self.Xw(X), dims="time")
        new_self.x.attrs["detrend"] = 1
        return new_self

    # modeling
    # ========

    def constant(self):
        return models.constant(self.time)

    def harmonics(self, period, n=1):
        return models.harmonics(self.time, period, n=n)

    def sinusoid(self, period):
        return self.harmonics(period)

    def Xw(self, X):
        w = np.linalg.lstsq(X, self.flux, rcond=None)[0]
        return X @ w

    def polynomial(self, **orders):
        return models.design_matrix([
            models.constant(self.time),
            *[models.polynomial(self.x[name].values, order) for name, order in orders.items() if order > 0]
        ])

    def split(self, dt):
        times = utils.split(self.x.time.values, dt)
        splits = [Flux(self.x.where((self.x.time >= st[0]) & (self.x.time <= st[-1]), drop=True)) for st in times]
        return splits
