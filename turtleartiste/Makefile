.PHONY: all clean

all: animation.gif giant-full.png

clean:
	rm -rf ps png gif animation.gif giant-*.png index.html

ps: turtle_artiste.py
	mkdir -p ps
	( cd ps; \
	../turtle_artiste.py )

png: ps
	mkdir -p png
	for file in ps/*.ps; do \
		echo $$file; \
		GS_FONTPATH="/Library/Fonts:/System/Library/Fonts:$$HOME/Library/Fonts" \
		gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m \
		-r600 -dDownScaleFactor=8 \
		-dEPSCrop \
		-dBackgroundColor="16#000000" \
		-sOutputFile=png/`basename $$file | cut -f 1 -d '.'`.png $$file; \
	done

gif: png
	mkdir -p gif
	for file in png/*.png; do \
		echo "Converting $$file"; \
		convert $$file gif/`basename $$file | cut -f 1 -d '.'`.gif; \
	done

animation.gif: gif
	gifsicle --colors 256 -d 10 -O3 gif/turtle-???.gif >animation.gif	

index.html: mkindex.py png
	./mkindex.py >index.html

giant-full.png: index.html
	webkit2png -W 1762 -H 6339 -o giant "file://$$(pwd)/index.html"
