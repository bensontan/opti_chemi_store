import sys

class opti_chemi_store(object):
	def __init__(self, xtrafee=79, entrycost=75, inccost=35, xchgpoints=6):
		self.xtrafee = xtrafee
		self.entrycost = entrycost
		self.inccost = inccost
		self.xchgpoints = xchgpoints
		self.maxdishes = {}

	def purchase_message(self, j, k, kleft, spent, left):
		return "Exchange {0} dishes and add {1} new points ({2} net points); spent {3} and left {4}\n".format(j, k, kleft, spent, left);

	def spend(self, cash=0, points=0):

		if (cash < self.entrycost) and (points < self.xchgpoints or cash < self.xtrafee):
			return [0, 0, 0, ''] # dish, point, cash spent, order sequence 

		cashpoints = str(cash) + '.' + str(points)

		# use a hash to record all caculated optimized results, to reduce redundant calculation 
		if self.maxdishes.has_key(cashpoints):
			return self.maxdishes[cashpoints]

		# in one step, you can either exchange dishes or purchase above the entrycost
		# so, exchange dishes has higher priority
		maxxchg = int(points / self.xchgpoints) + 1 

		purchasedishes = []

		for j in xrange(maxxchg):
			currspend = self.xtrafee * j # spent on xchange to dishes
			currcash = cash - currspend

			# no money to exchange to dishes (gift)
			if currcash < 0:
				break 

			currdish = j
			# points after exchange
			currpoints = points - self.xchgpoints * j + max(int((currspend - self.entrycost) / self.inccost), 0)

			i = 0 # additional money will be spent
			k = 0 # points will be exchanged
			while (i < currcash):
				if j > 0 or i != 0:
					ret = self.spend(currcash - i, currpoints + k)

					purchasedishes.append([
						currdish + ret[0], # dish
						currpoints + k - points + ret[1], # points
						currspend + i + ret[2], # cash spent
						self.purchase_message( # order sequence
							j, # exchange dishes
							currpoints + k - points + j * self.xchgpoints, # new points
							currpoints + k, # net points
							currspend + i, # spent
							cash - currspend - i) + # left 
							ret[3]]) # the left steps from the remaining money thru recursive calls

				# calculate for next amount of spends to get next point
				i = max(int((i + currspend - self.entrycost) / self.inccost + 1), 0) * self.inccost + self.entrycost - currspend
				k = k + 1

		# if has points but not enough money to exchange
		if len(purchasedishes) == 0: 
			return [0, 0, 0, '']

		# find the best solution for this amount of cash
		foundndx = 0
		for ndx in xrange(len(purchasedishes)):
			if purchasedishes[ndx][0] < purchasedishes[foundndx][0]:
				continue
			elif purchasedishes[ndx][0] == purchasedishes[foundndx][0]:
				if purchasedishes[ndx][1] < purchasedishes[foundndx][1]:
					continue
				elif purchasedishes[ndx][1] == purchasedishes[foundndx][1]:
					if purchasedishes[ndx][2] > purchasedishes[foundndx][2]:
						continue
			foundndx = ndx

		self.maxdishes[cashpoints] = purchasedishes[foundndx]

		return self.maxdishes[cashpoints]


if __name__ == '__main__':
	if len(sys.argv) > 1:
		money = int(sys.argv[1])
	else:
		money = 1000

	s = opti_chemi_store()
	r = s.spend(money)
	print('Budget: ' + str(money))
	print('Max gift could get: ' + str(r[0]))
	print('Max points could collect after collect gift: ' + str(r[1]))
	print('Total money spent: ' + str(r[2]))
	print('Details:')
	print(r[3])
