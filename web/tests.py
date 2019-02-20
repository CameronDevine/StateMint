from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
import unittest
import json
from urllib import quote
from urllib import unquote
import os
import piexif
import io
from threading import Thread
from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from copy import deepcopy

class MyHandler(SimpleHTTPRequestHandler):
	def log_message(self, *arg, **kwargs):
		return

server = HTTPServer(('', 80), MyHandler)
thread = Thread(target = server.serve_forever)
thread.daemon = True
thread.start()

options = ChromeOptions()
options.add_argument('no-sandbox')
options.add_argument('headless')
options.add_experimental_option('prefs', {
	'download.default_directory': os.getcwd()
})

class Timeout(Exception):
	pass

url = 'http://localhost/HTML'

sharedata = "/?%7B%22InVars%22%3A%22Vs%22%2C%22StVarElEqns%22%3A%22tk%27%20%3D%20kt%20*%20wk%22%2C%22OtherElEqns%22%3A%22vR%20%3D%20R%20*%20iR%2C%5CnvL%20%3D%20L%20*%20iL%27%2C%5Cni1%20%3D%20-Kv%20*%20t2%2C%5Cnw2%20%3D%20Kv%20*%20v1%2C%5Cnw3%20%3D%20Q4%20%2F%20-D%2C%5CnP4%20%3D%20t3%20%2F%20D%2C%5CnQR%20%3D%20PR%20%2F%20Rf%22%2C%22Constraints%22%3A%22iL%20%3D%20i1%2C%5CniR%20%3D%20i1%2C%5Cnt2%20%3D%20-tk%2C%5Cnt3%20%3D%20tk%2C%5CnQ4%20%3D%20QR%2C%5Cnv1%20%3D%20Vs%20-%20vR%20-%20vL%2C%5Cnwk%20%3D%20w2%20-%20w3%2C%5CnPR%20%3D%20P4%22%2C%22OutputVars%22%3A%22QR%22%7D"

tutorial = {
	"InVars": "Vs",
	"StVarElEqns": "tk' = kt * wk",
	"OtherElEqns": "vR = R * iR,\nvL = L * iL',\ni1 = -Kv * t2,\nw2 = Kv * v1,\nw3 = Q4 / -D,\nP4 = t3 / D,\nQR = PR / Rf",
	"Constraints": "iL = i1,\niR = i1,\nt2 = -tk,\nt3 = tk,\nQ4 = QR,\nv1 = Vs - vR - vL,\nwk = w2 - w3,\nPR = P4",
	"OutputVars": "QR",
}

import time

class MyChrome(Chrome):
	def window_inner_height(self):
		return self.execute_script('return window.innerHeight;')
	def page_y_offset(self):
		return self.execute_script('return window.pageYOffset;')
	def hover(self, element):
		ActionChains(self).move_to_element(element).perform()
	def wait(self, d = 0.5):
		time.sleep(d)
	def show(self, selector):
		self.execute_script('$("{}").show();'.format(selector))
	def hide(self, selector):
		self.execute_script('$("{}").hide();'.format(selector))

examples = [{
	"InVars": "vS",
	"StVarElEqns": "vMB' = 1/MB * fMB,\nvMW' = 1/MW * fMW,\nfKS' = KS * vKS,\nfKT' = KT * vKT",
	"OtherElEqns": "fBS = BS * vBS,\nfBT = BT * vBT",
	"Constraints": "fMB = fKS + fBS,nfMW = fKT + fBT - fKS - fBS,\nvKS = vMW - vMB,\nvKT = vS - vMW,\nvBS = vMW - vMB,\nvBT = vS - vMW",
	"OutputVars": "vMB, vMW, fKS, fKT, fBS, fBT",
	}, {
	"InVars": "Fs",
	"StVarElEqns": "vm' = Fm/m,\nFK1' = K1 * vK1",
	"OtherElEqns": "FB2 = B2 * vB2,\nvB1 = FB1/B1,\nvK2 = FK2' / K2",
	"Constraints": "vK1 = vK2 - vB1,\nvB2 = vm,\nFK2 = Fs - FK1,\nFB1 = FK1,\nFm = Fs - FB2",
	"OutputVars": "vB1",
	}, {
	"InVars": "Fp, F0",
	"StVarElEqns": "vm' = Fm / m",
	"OtherElEqns": "Fd = cd * vd**2",
	"Constraints": "Fm = Fp - F0 - Fd,\nvd = vm",
	"OutputVars": "vm"
}]

example_data = [{
	'nonlinear': False,
	'nonstandard': False,
	}, {
	'nonlinear': False,
	'nonstandard': True,
	}, {
	'nonlinear': True,
	'nonstandard': False,
}]

output_forms = {
	'equation': {
		'vector': ['State Vector', 'Input Vector', 'Output Vector'],
		'StateSpace': ['State', 'Output'],
		'StateSpaceN': ['State', 'Output'],
		'StateSpaceP': ['State', 'Output'],
		'eq': ['State', 'Output'],
		'TF': ['Transfer Function']},
	'latex': {
		'vector': ['State Vector', 'Input Vector', 'Output Vector'],
		'StateSpace': ['A', 'B', 'C', 'D'],
		'StateSpaceN': ['A', 'B', 'C', 'D', 'E', 'F'],
		'StateSpaceP': ['A', "B'", 'C', "D'"],
		'eq': ['State Equation', 'Output Equation'],
		'TF': ['Transfer Function']},
	'matlab': {
		'StateSpace': ['A', 'B', 'C', 'D'],
		'StateSpaceN': ['A', 'B', 'C', 'D', 'E', 'F'],
		'StateSpaceP': ['A', "B'", 'C', "D'"]},
	'mathematica': {
		'StateSpace': ['State Equation Matricies'],
		'StateSpaceN': ['State Equation Matricies'],
		'StateSpaceP': ['State Equation Matricies'],
		'eq': ['State Equation', 'Output Equation']},
	'python': {
		'StateSpace': ['A', 'B', 'C', 'D'],
		'StateSpaceN': ['A', 'B', 'C', 'D', 'E', 'F'],
		'StateSpaceP': ['A', "B'", 'C', "D'"],
		'eq': ['State Equation', 'Output Equation']}
}

class TestWebInterface(unittest.TestCase):
	def setUp(self):
		self.driver = MyChrome(chrome_options = options)
		self.driver.get(url)

	def tearDown(self):
		self.driver.quit()
		try:
			os.remove('system.rnd')
		except OSError:
			pass

	def example_test(self, num):
		self.driver.wait()
		self.driver.find_element('link text', 'examples').click()
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'page4').is_displayed())
		self.assertEqual(self.driver.page_y_offset(), self.driver.window_inner_height())
		self.driver.hover(self.driver.find_element('link text', 'EXAMPLE {}'.format(num)))
		self.assertEqual(self.driver.find_element('id', 'exampleImage').get_attribute('src').split('/')[-1], 'example{}.svg'.format(num))
		self.driver.find_element('id', 'page4').find_element('class name', 'smooth').click()
		self.driver.wait()
		self.assertEqual(self.driver.page_y_offset(), 2 * self.driver.window_inner_height())
		self.assertTrue(self.driver.find_element('id', 'systemImage').is_displayed())
		example = examples[num - 1]
		for key in example:
			self.assertEqual(self.driver.find_element('id', key).get_attribute('value'), example[key])
		self.driver.find_element('id', 'page5').find_element('class name', 'btn').click()
		self.driver.wait()
		timeout = True
		for i in range(int(10 / 0.2)):
			if self.driver.find_element('id', 'page6').is_displayed():
				timeout = False
				break
			self.driver.wait(0.2)
		if timeout:
			raise Timeout
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'page6').is_displayed())
		self.driver.wait()
		self.assertFalse(self.driver.find_element('id', 'LoadingPage').is_displayed())
		self.results_test(num)

	def results_test(self, example_num):
		output_form = deepcopy(output_forms)
		if example_data[example_num - 1]['nonlinear']:
			if 'matlab' in output_form:
				del output_form['matlab']
			for lang in output_form:
				if 'TF' in output_form[lang]:
					del output_form[lang]['TF']
		else:
			for lang in output_form:
				if 'eq' in output_form[lang]:
					del output_form[lang]['eq']
		if example_data[example_num - 1]['nonstandard']:
			for lang in output_form:
				if 'StateSpace' in output_form[lang]:
					del output_form[lang]['StateSpace']
		else:
			for lang in output_form:
				if 'StateSpaceN' in output_form[lang]:
					del output_form[lang]['StateSpaceN']
				if 'StateSpaceP' in output_form[lang]:
					del output_form[lang]['StateSpaceP']
		lang_buttons = self.driver.find_element('id', 'langButtons').find_elements('tag name', 'button')
		self.assertEqual(
			sum([el.is_displayed() for el in lang_buttons]),
			len(output_form))
		for lang in lang_buttons:
			if lang.is_displayed():
				lang_name = lang.text.lower()
				lang_output_form = output_form[lang_name]
				self.assertIn(lang_name, output_form)
				lang.click()
				self.driver.wait()
				eq_buttons = self.driver.find_element('id', 'eqButtons').find_elements('tag name', 'button') 
				self.assertEqual(
					sum([el.is_displayed() for el in eq_buttons]), 
					len(lang_output_form),
					'button ids: {}, desired: {}'.format([el.get_attribute('id') for el in eq_buttons if el.is_displayed()], lang_output_form.keys()))
				for eq in eq_buttons:
					if eq.is_displayed():
						eq_id = eq.get_attribute('id')
						eq_output_form = lang_output_form[eq_id]
						self.assertIn(eq_id, lang_output_form)
						eq.click()
						outputs = self.driver.find_element('id', 'output').find_elements('class name', 'buttons')
						self.assertEqual(
							sum([el.is_displayed() for el in outputs]),
							len(eq_output_form))
						for out, title in zip(outputs, eq_output_form):
							self.assertEqual(out.find_element('tag name', 'h4').text, title)

	def modal_test(self, open_link, id, partial = False, test_content = False):
		open_link.click()
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', id).is_displayed())
		if test_content:
			self.assertNotEqual(len(self.driver.find_element('id', id).find_element('class name', 'markdown').text), 0)
		self.driver.find_element('id', id).find_element('class name', 'close').click()
		self.driver.wait()
		if not partial:
			self.assertFalse(self.driver.find_element('id', id).is_displayed())
			open_link.click()
			self.driver.wait()
			self.assertTrue(self.driver.find_element('id', id).is_displayed())
			self.driver.find_element('id', id).find_element('class name', 'btn-default').click()
			self.driver.wait()
			self.assertFalse(self.driver.find_element('id', id).is_displayed())

	def command_test(self, open_link, partial = False):
		open_link.click()
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'commandRef').is_displayed())
		self.driver.find_element('id', 'commandRef').find_element('class name', 'close').click()
		self.driver.wait()
		if not partial:
			self.assertFalse(self.driver.find_element('id', 'commandRef').is_displayed())
			open_link.click()
			self.driver.wait()
			self.assertTrue(self.driver.find_element('id', 'commandRef').is_displayed())
			self.driver.find_element('id', 'commandRef').find_element('class name', 'btn-default').click()
			self.driver.wait()
			self.assertFalse(self.driver.find_element('id', 'commandRef').is_displayed())

	def test_example1(self):
		self.example_test(1)

	def test_example2(self):
		self.example_test(2)

	def test_example3(self):
		self.example_test(3)

	def test_tutorial1(self):
		self.modal_test(self.driver.find_elements('link text', 'tutorial')[0], 'tutorialRef', test_content = True)

	def test_tutorial2(self):
		self.driver.find_element('link text', 'examples').click()
		self.driver.wait()
		self.modal_test(self.driver.find_elements('link text', 'tutorial')[1], 'tutorialRef', test_content = True)

	def test_tutorial3(self):
		self.modal_test(self.driver.find_element('class name', 'help-block').find_elements('link text', 'here')[1], 'tutorialRef', test_content = True)

	def test_command1(self):
		self.driver.find_element('link text', 'examples').click()
		self.driver.wait()
		self.modal_test(self.driver.find_element('link text', 'syntax'), 'commandRef')

	def test_command2(self):
		self.driver.find_element('link text', 'examples').click()
		self.driver.wait()
		self.modal_test(self.driver.find_element('class name', 'help-block').find_elements('link text', 'here')[0], 'commandRef')

	def test_tooltips(self):
		self.driver.find_element('id', 'page3button').click()
		self.driver.wait()
		for key in examples[0]:
			self.driver.hover(self.driver.find_element('id', key))
			tooltip_id = self.driver.find_element('id', key).get_attribute('aria-describedby')
			self.assertTrue(self.driver.find_element('id', tooltip_id).is_displayed())
			if key == 'StVarElEqns':
				self.modal_test(self.driver.find_element('id', tooltip_id).find_element('link text', 'tutorial'), 'tutorialRef', partial = True)
			elif key == 'OtherElEqns':
				self.modal_test(self.driver.find_element('id', tooltip_id).find_element('link text', 'command reference'), 'commandRef', partial = True)
			self.driver.hide('#' + tooltip_id)

	def test_share_load(self):
		self.driver.get(url + sharedata)
		for key in tutorial:
			self.assertEqual(self.driver.find_element('id', key).get_attribute('value'), tutorial[key])
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'LoadingPage').is_displayed())
		self.assertScroll('LoadingPage')
		timeout = True
		for i in range(int(10 / 0.2)):
			if self.driver.find_element('id', 'page6').is_displayed():
				timeout = False
				break
			self.driver.wait(0.2)
		if timeout:
			raise Timeout
		self.assertTrue(self.driver.find_element('id', 'page6').is_displayed())

	def test_share_copy(self):
		self.driver.find_element('link text', 'examples').click()
		self.driver.wait()
		self.driver.hover(self.driver.find_element('link text', 'EXAMPLE 1'))
		self.driver.show('#page6')
		self.driver.find_element('partial link text', 'SHARE').click()
		self.driver.show('#shareArea')
		copy = unquote(self.driver.find_element('id', 'shareArea').get_attribute('value'))
		self.assertTrue(json.loads(copy[copy.find('/?') + 2:]) == examples[0])

	def test_save(self):
		self.driver.delete_all_cookies()
		self.driver.find_element('link text', 'examples').click()
		self.driver.wait()
		self.driver.hover(self.driver.find_element('link text', 'EXAMPLE 1'))
		self.driver.show('#page6')
		self.driver.find_element('partial link text', 'SAVE').click()
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'saveRef').is_displayed())
		self.driver.find_element('id', 'saveRef').find_element('class name', 'close').click()
		self.driver.wait()
		self.assertFalse(self.driver.find_element('id', 'saveRef').is_displayed())
		self.driver.find_element('partial link text', 'SAVE').click()
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'saveRef').is_displayed())
		self.driver.find_element('id', 'saveRef').find_element('class name', 'btn-default').click()
		self.driver.wait()
		self.assertFalse(self.driver.find_element('id', 'saveRef').is_displayed())
		self.driver.find_element('partial link text', 'SAVE').click()
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'saveRef').is_displayed())
		self.driver.find_element('id', 'saveName').send_keys('test')
		self.driver.find_element('id', 'saveRef').find_element('class name', 'btn-primary').click()
		self.driver.wait()
		self.assertFalse(self.driver.find_element('id', 'saveRef').is_displayed())
		cookies = self.driver.get_cookies()
		self.assertEqual(len(cookies), 1)
		cookie = cookies[0]
		self.assertEqual(cookie['name'], 'stmt_test')
		self.assertEqual(json.loads(unquote(cookie['value'])), examples[0])

	def test_load(self):
		self.driver.find_element('id', 'page1').find_element('class name', 'btn-default').click()
		self.assertFalse(self.driver.find_element('id', 'saved').is_displayed())
		self.driver.add_cookie({
			'name': 'stmt_test2',
			'value': quote(json.dumps(examples[1]))
		})
		self.driver.refresh()
		self.driver.find_element('id', 'page1').find_element('class name', 'btn-default').click()
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'saved').is_displayed())
		self.assertEqual(len(self.driver.find_element('id', 'saved').find_elements('tag name', 'tr')), 1)
		self.assertEqual(self.driver.find_element('id', 'saved').find_element('tag name', 'strong').text, 'test2')
		self.driver.find_element('id', 'saved').find_elements('tag name', 'td')[0].click()
		timeout = True
		for i in range(int(10 / 0.2)):
			if self.driver.find_element('id', 'page6').is_displayed():
				timeout = False
				break
			self.driver.wait(0.2)
		if timeout:
			raise Timeout
		self.assertTrue(self.driver.find_element('id', 'page6').is_displayed())
		self.driver.refresh()
		self.driver.find_element('id', 'page1').find_element('class name', 'btn-default').click()
		self.driver.wait()
		self.driver.find_element('id', 'saved').find_elements('tag name', 'td')[1].click()
		timeout = True
		for i in range(int(10 / 0.2)):
			if self.driver.find_element('id', 'page6').is_displayed():
				timeout = False
				break
			self.driver.wait(0.2)
		if timeout:
			raise Timeout
		self.assertTrue(self.driver.find_element('id', 'page6').is_displayed())

	def test_delete(self):
		self.driver.add_cookie({
			'name': 'stmt_test2',
			'value': quote(json.dumps(examples[1]))
		})
		self.driver.refresh()
		self.driver.find_element('id', 'page1').find_element('class name', 'btn-default').click()
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'saved').is_displayed())
		self.driver.find_element('id', 'saved').find_elements('tag name', 'td')[2].click()
		self.assertFalse(self.driver.find_element('id', 'saved').is_displayed())
		self.assertEqual(len(self.driver.get_cookies()), 0)

	def test_add_image(self):
		self.driver.find_element('id', 'fileUploadHidden').send_keys(os.getcwd() + '/HTML/examples/example1.jpg')
		self.driver.wait()
		self.assertTrue(len(self.driver.find_element('id', 'systemImage').get_attribute('src')) > 0)
		self.assertTrue(self.driver.find_element('id', 'systemImage').is_displayed())

	@unittest.expectedFailure
	def test_download(self):
		self.driver.find_element('link text', 'examples').click()
		self.driver.wait()
		self.driver.hover(self.driver.find_element('link text', 'EXAMPLE 1'))
		self.driver.show('#page6')
		self.driver.wait()
		self.driver.find_element('id', 'page6').find_elements('class name', 'btn')[-1].click()
		timeout = True
		for i in range(int(10 / 0.2)):
			if os.isfile('system.rnd'):
				timeout = False
				break
			self.driver.wait(0.2)
		if timeout:
			raise Timeout
		self.assertEqual(json.loads(piexif.load('system.rnd')['Exif'][37510]), examples[0])

	def test_upload(self):
		with open('HTML/examples/example3.jpg', 'rb') as f:
			jpeg = f.read()
		rnd = io.BytesIO()
		piexif.insert(piexif.dump({'Exif': {37510: json.dumps(examples[2])}}), jpeg, rnd)
		with open('system.rnd', 'wb') as f:
			f.write(rnd.read())
		self.driver.find_element('id', 'page1').find_element('class name', 'btn-default').click()
		self.driver.find_element('id', 'fileUploadLink').send_keys(os.getcwd() + '/system.rnd')
		timeout = True
		for i in range(int(10 / 0.2)):
			if self.driver.find_element('id', 'page6').is_displayed():
				timeout = False
				break
			self.driver.wait(0.2)
		if timeout:
			raise Timeout
		self.driver.wait(1)
		self.assertTrue(self.driver.find_element('id', 'page6').is_displayed())
		self.driver.find_element('id', 'page3button').click()
		self.driver.wait()
		self.assertTrue(len(self.driver.find_element('id', 'systemImage').get_attribute('src')) > 0)
		self.assertTrue(self.driver.find_element('id', 'systemImage').is_displayed())

	def page_location(self, page_id):
		page_ids = ['page1', 'page2', 'page3', 'page4', 'page5', 'page6button', 'LoadingPage', 'page6']
		loc = 0
		for pid in page_ids:
			if pid == page_id:
				break
			if self.driver.find_element('id', pid).is_displayed():
				loc += self.driver.find_element('id', pid).size['height']
		return loc

	def assertScroll(self, page_id):
		self.assertEqual(self.page_location(page_id), self.driver.page_y_offset())

	def assertDotSize(self, ind):
		dots = self.driver.find_element('class name', 'scrolling').find_elements('tag name', 'li')
		for i, dot in enumerate(dots):
			dot_class = dot.get_attribute('class')
			if i == ind:
				self.assertEqual(dot_class, 'activeDot')
			else:
				self.assertEqual(dot_class, '')

	def test_scroll(self):
		self.driver.wait(1.5)
		dots = self.driver.find_element('class name', 'scrolling').find_elements('tag name', 'li')
		self.assertTrue(self.driver.find_element('id', 'page2').is_displayed())
		self.assertFalse(self.driver.find_element('id', 'page3').is_displayed())
		self.assertFalse(self.driver.find_element('id', 'page4').is_displayed())
		self.assertFalse(self.driver.find_element('id', 'LoadingPage').is_displayed())
		self.assertFalse(self.driver.find_element('id', 'page6').is_displayed())
		self.assertEqual(
			sum([el.is_displayed() for el in dots]),
			3)
		self.assertDotSize(0)
		self.assertScroll('page1')
		self.driver.find_element('id', 'page1').find_element('class name', 'social-icons').find_element('tag name', 'a').click()
		self.driver.wait()
		self.assertDotSize(1)
		self.assertScroll('page2')
		self.driver.find_element('id', 'page2').find_element('class name', 'social-icons').find_element('tag name', 'a').click()
		self.driver.wait()
		self.assertDotSize(2)
		self.assertScroll('page5')
		self.assertFalse(self.driver.find_element('id', 'page6button').find_element('tag name', 'a').is_displayed())
		dots[1].click()
		self.driver.wait()
		self.assertDotSize(1)
		self.assertScroll('page2')
		dots[0].click()
		self.driver.wait()
		self.assertDotSize(0)
		self.assertScroll('page1')
		self.driver.find_element('link text', 'examples').click()	
		self.driver.wait()
		self.assertFalse(self.driver.find_element('id', 'page2').is_displayed())
		self.assertFalse(self.driver.find_element('id', 'page3').is_displayed())
		self.assertTrue(self.driver.find_element('id', 'page4').is_displayed())
		self.assertDotSize(1)
		self.assertScroll('page4')
		dots[0].click()
		self.driver.wait()
		self.assertDotSize(0)
		self.assertScroll('page1')
		dots[1].click()
		self.driver.wait()
		self.assertDotSize(1)
		self.assertScroll('page4')
		dots[0].click()
		self.driver.wait()
		self.assertDotSize(0)
		self.assertScroll('page1')
		self.driver.find_element('id', 'page1').find_element('class name', 'social-icons').find_element('tag name', 'a').click()
		self.driver.wait()
		self.assertDotSize(1)
		self.assertScroll('page4')
		self.driver.find_element('link text', 'EXAMPLE 1').click()
		self.driver.wait()
		self.assertDotSize(2)
		self.assertScroll('page5')
		dots[1].click()
		self.driver.wait()
		self.assertDotSize(1)
		self.assertScroll('page3')
		self.driver.find_element('link text', 'EXAMPLE 2').click()
		self.driver.wait()
		self.assertDotSize(2)
		self.assertScroll('page5')
		dots[1].click()
		self.driver.wait()
		self.driver.find_element('link text', 'EXAMPLE 3').click()
		self.driver.wait()
		self.assertDotSize(2)
		self.assertScroll('page5')
		self.driver.find_element('id', 'page5').find_element('class name', 'btn').click()
		self.driver.wait(0.3)
		self.assertTrue(self.driver.find_element('id', 'LoadingPage').is_displayed())
		self.assertScroll('LoadingPage')
		timeout = True
		for i in range(int(10 / 0.2)):
			if self.driver.find_element('id', 'page6').is_displayed():
				timeout = False
				break
			self.driver.wait(0.2)
		if timeout:
			raise Timeout
		self.driver.wait(1)
		self.assertFalse(self.driver.find_element('id', 'LoadingPage').is_displayed())
		self.assertTrue(self.driver.find_element('id', 'page6').is_displayed())
		self.assertTrue(self.driver.find_element('id', 'page6button').find_element('tag name', 'a').is_displayed())
		self.assertDotSize(3)
		self.assertScroll('page6')
		self.assertEqual(
			sum([el.is_displayed() for el in dots]),
			4)
		dots[0].click()
		self.driver.wait()
		self.assertDotSize(0)
		self.assertScroll('page1')
		dots[3].click()
		self.driver.wait()
		self.assertDotSize(3)
		self.assertScroll('page6')
		dots[2].click()
		self.driver.wait()
		self.assertDotSize(2)
		self.assertScroll('page5')
		self.driver.find_element('id', 'page6button').click()
		self.driver.wait()
		self.assertDotSize(3)
		self.assertScroll('page6')
		dots[0].click()
		self.driver.wait()
		self.assertDotSize(0)
		self.assertScroll('page1')
		self.driver.find_element('link text', 'CREATE NEW MODEL').click()
		self.driver.wait()
		self.assertTrue(self.driver.find_element('id', 'page2').is_displayed())
		self.assertFalse(self.driver.find_element('id', 'page3').is_displayed())
		self.assertFalse(self.driver.find_element('id', 'page4').is_displayed())
		self.assertDotSize(1)
		self.assertScroll('page2')
		dots[0].click()
		self.driver.wait()
		self.assertDotSize(0)
		self.assertScroll('page1')
		dots[1].click()
		self.driver.wait()
		self.assertDotSize(1)
		self.assertScroll('page2')
		dots[0].click()
		self.driver.wait()
		self.assertDotSize(0)
		self.assertScroll('page1')
		self.driver.find_element('id', 'page1').find_element('tag name', 'button').click()
		self.driver.wait()
		self.assertFalse(self.driver.find_element('id', 'page2').is_displayed())
		self.assertTrue(self.driver.find_element('id', 'page3').is_displayed())
		self.assertFalse(self.driver.find_element('id', 'page4').is_displayed())
		self.assertDotSize(1)
		self.assertScroll('page3')
		dots[0].click()
		self.driver.wait()
		self.assertDotSize(0)
		self.assertScroll('page1')
		dots[1].click()
		self.driver.wait()
		self.assertDotSize(1)
		self.assertScroll('page3')
		dots[0].click()
		self.driver.wait()
		self.assertDotSize(0)
		self.assertScroll('page1')
		self.driver.find_element('id', 'page1').find_element('class name', 'social-icons').find_element('tag name', 'a').click()
		self.driver.wait()
		self.assertDotSize(1)
		self.assertScroll('page3')

if __name__ == '__main__':
	unittest.main()
