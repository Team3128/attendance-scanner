from report_generator import ReportGenerator

new_scans_path = "newscans.csv"

season = "2018-19"

total_start = "2018-09-07"
total_end = "2019-06-14"

build_start = "2019-01-05"
build_end = "2019-02-19"

report_generator = ReportGenerator(new_scans_path, season, total_start, total_end, build_start, build_end)
report_generator.update()