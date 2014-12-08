#ChartGenerator.py

#this class takes aggregated check data and generates an SVG chart using pygal 

import pygal
import os
import shutil

    
class ChartGenerator():
        
    def __init__(self, location):
        self.config = pygal.Config()
        self.custom_config(self.config)
        self.chart_location = location + 'chart.svg'
        self.backup_location = location + 'chart_files/backups/'
        
    def custom_config(self, config):
        config.show_legend = False
        config.human_readable = True
        config.fill = True
        config.label_font_size = 24
        config.major_label_font_size = 24

    def generate_chart(self, check_round,  teams):
        #first, set the title dynamically
        self.config.title = 'Scoring as of round ' + str(check_round)
        
        #create a chart object with special settings declared in customConfig()
        chart = pygal.Bar(self.config)
        
        #add each team's score to chart        
        for team in teams:
            bar_count = team.getId()
            score = team.getScore()
            chart.add('Team ' + str(bar_count) + ' score', [{'value': score, 'label': 'Team ' + str(bar_count)}])

        self.make_chart_backup(check_round)
        #we have a chart! put it somewhere accessible.
        chart.render_to_file(self.chart_location)

    def make_chart_backup(self, check_round):
        if not os.path.exists(self.backup_location):
            os.makedirs(self.backup_location)

        shutil.move(self.chart_location, self.backup_location + 'chart_' + str(check_round) + '.svg')