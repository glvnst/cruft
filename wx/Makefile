.PHONY: all testrun clean

all: pep8.txt pylint.txt testrun

testrun:
	@echo "==> Running test"
	./wx.py -u f 12797325

clean:
	@echo "==> Cleaning"
	rm -f forecast.xml wx.pyc wx.html pep8.txt pylint.txt

# Used during the development phase
forecast.xml:
	wget -O forecast.xml "http://weather.yahooapis.com/forecastrss?w=12797325&u=f"

# Used to generate docs, etc.
wx.html:
	htmlizer wx.py wx.html

pep8.txt: wx.py
	@echo "==> PEP8"
	pep8 wx.py >pep8.txt

pylint.txt: wx.py
	@echo "==> PyLint"
	pylint wx.py > pylint.txt 2>/dev/null; true
	@grep "code has been rated" pylint.txt