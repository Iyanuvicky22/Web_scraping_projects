import billboard


chart = billboard.ChartData('hot-100', year=2024)
for entry in chart:
    print(entry.rank, entry.title, entry.artist)
