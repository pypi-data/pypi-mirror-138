if __name__ == '__main__':
	print('nope')

class ThirtyFile:
	_transposes = {
		'bup': -3,
		'bong': 2,
		'gnome': 4,
		'🔔': 3,
		'🚫': 6,
		'🚨': 7,
		'🦴': 4,
		'🦢': 2,
		'builttoscale': 6,
		'samurai': -3,
		'mariopaint_cat': 1,
		'mariopaint_dog': 1,
		'buzzer': -4,
		'ultrainstinct': -3
	}
	
	def __init__(self):
		self.events = []

	def placeNote(self, inst, transpose=0, combine=False):
		if (inst in ThirtyFile._transposes):
			transpose += ThirtyFile._transposes[inst]
		if (combine == True):
			self.combine()
		self.events.append(ThirtyEvent(inst, None if transpose == 0 else transpose, True))

	def combine(self):
		self.events.append(ThirtyEvent('combine'))

	def setTempo(self, bpm):
		self.events.append(ThirtyEvent('speed', int(bpm)))

	def pause(self, beats=1):
		if (int(beats) > 0):
			self.events.append(ThirtyEvent('stop', int(beats)))

	def repeat(self, times=1):
		thousands = times // 1000
		for i in range(thousands):
			self.events.append(ThirtyEvent('loopmany', 1000))
		self.events.append(ThirtyEvent('loopmany', int(times % 1000)))

	def save(self, filename):
		with open(filename, 'w') as f:
			things = [str(s) for s in self.events]
			f.write('|'.join(things))

class ThirtyEvent:
	def __init__(self, name, value=None, isNote=False):
		self.name = name
		self.value = value
		self.isNote = isNote

	def __str__(self):
		ret = "" if (self.isNote) else "!"
		ret += self.name
		if (self.value is not None):
			ret += "@" + str(self.value)
		return ret