from prose import FitsManager, pipeline

fm = FitsManager("/Users/lionelgarcia/Downloads/part1")

calib = pipeline.Calibration(images=fm.images)
calib.run(fm.obs_name)