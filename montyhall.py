import webapp2
import jinja2
import os
import random
import json

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class IndexPage(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class Results(webapp2.RequestHandler):
    def get(self):
        '''
        Runs 'num' iterations of the Monty Hall problem simulation
        and returns the results. Intended to be run many times.
        '''
        iterations = int(self.request.get('num', '10'))
        results = []

        for i in range(iterations):
            winning_choice = random.randrange(1, 4)
            initial_choice = random.randrange(1, 4)

            # figure out what the switching player would do
            reveal_doors = [1, 2, 3]
            reveal_doors.remove(winning_choice)
            if initial_choice in reveal_doors:
                reveal_doors.remove(initial_choice)
            revealed_choice = random.choice(reveal_doors)

            switch_doors = [1, 2, 3]
            switch_doors.remove(initial_choice)
            if revealed_choice in switch_doors:
                switch_doors.remove(revealed_choice)
            switch_choice = random.choice(switch_doors)

            results.append({
                'initial_choice': initial_choice,
                'revealed_choice': revealed_choice,
                'switch_choice': switch_choice,
                'winning_choice': winning_choice
            })

        self.response.out.write(json.dumps(results))

app = webapp2.WSGIApplication([('/', IndexPage),
                               ('/results', Results)],
                              debug=True)