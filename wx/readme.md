# wx

Report weather conditions for yahoo WOEID(s) to the terminal. Can report in Celsius or Fahrenheit.

## Usage

`wx [-h] [-u {c,f}] woeid [woeid ...]`

Where woeid is one or more yahoo WOEID ("where on earth ID") to report on. Optional arguments include a `-u` units specifier, which takes an argument of either `f` for Fahrenheit or `c` for Celsius.

## Notes

The data at our target URL (at the time of design) looks like this:

```
...
<yweather:location city="Twin Peaks" region="WA"   country="United States"/>
<yweather:units temperature="F" distance="mi" pressure="in" speed="mph"/>
<yweather:wind chill="66"   direction="290"   speed="14" />
<yweather:atmosphere humidity="63" visibility="10" pressure="30.09> rising="0"/>
<yweather:astronomy sunrise="7:24 am"   sunset="7:13 pm"/>
<yweather:condition  text="Partly Cloudy"  code="30"  temp="66> date="Tue, 12 Mar 2013 4:52 pm PDT" />
<yweather:forecast day="Tue" date="12 Mar 2013" low="50" high="72> text="Mostly Clear" code="33" />
<yweather:forecast day="Wed" date="13 Mar 2013" low="52" high="75> text="Partly Cloudy" code="30" >
...

```

## License

This code is licensed under a BSD-style license. See license.txt for details.

## Todo

- Support US Zip-code lookups