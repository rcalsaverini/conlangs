LEXURGY := ../../../../../../bin/lexurgy/bin/lexurgy sc
SOUND_CHANGES := pie.lsc
WORDS_FILE := words.wli

watch:
	watchman-make -p '**/{pie.lsc,words}' -t run

.PHONY: run

run:
	$(LEXURGY) $(SOUND_CHANGES) $(WORDS_FILE)