from functools import partial

from kivy.app import App
from kivyblocks.blocks import Blocks
from kivyblocks import toggleitems
from kivy.uix.boxlayout import BoxLayout

class TestApp(App):
	def build(self):
		desc = {
			"widgettype":"ToggleItems",
			"options":{
				"spacing":40,
				"border_width":4,
				"items_desc":[
					{
						"widgettype":"Label",
						"options":{
							"text":"Item 2"
						}
					},{
						"widgettype":"Label",
						"options":{
							"text":"Item 1"
						}
					},{
						"widgettype":"Label",
						"options":{
							"text":"Item 3"
						}
					}
				]
			}
		}
		box = BoxLayout()
		blocks = Blocks()
		def cb(parent_widget,o,w):
			parent_widget.add_widget(w)

		blocks.bind(on_built=partial(cb,box))
		blocks.widgetBuild(desc)
		return box

if __name__ == '__main__':
	TestApp().run()
