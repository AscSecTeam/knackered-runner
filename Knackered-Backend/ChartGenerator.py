#ChartGenerator.py

#this class takes aggregated check data and generates an SVG chart using pygal 

import pygal
import os
import shutil

    
class ChartGenerator():
        
    def __init__(self):
        self.config = pygal.Config()
        self.custom_config(self.config)
        
    def custom_config(self, config):
        config.show_legend = False
        config.human_readable = True
        config.fill = True
        config.label_font_size = 24
        config.major_label_font_size = 24

    def generate_chart(self, save_location, check_round,  score_array):
        #first, set the title dynamically
        self.config.title = 'Scoring as of round ' + str(check_round)
        
        #create a chart object with special settings declared in customConfig()
        chart = pygal.Bar(self.config)
        
        #add each team's score to chart        
        bar_count = 1
        for score in score_array:
            chart.add('Team ' + str(bar_count) + ' score', [{'value': score, 'label': 'Team ' + str(bar_count)}])
            bar_count += 1

        self.make_chart_backup(check_round)
        #we have a chart! put it somewhere accessible.
        chart.render_to_file(save_location)

    def make_chart_backup(self, check_round):
        directory = '/var/www/html/chart_files/backups/'
        if not os.path.exists(directory):
            os.makedirs(directory)

        shutil.move('/var/www/html/chart.svg', directory + 'chart_' + str(check_round) + '.svg')