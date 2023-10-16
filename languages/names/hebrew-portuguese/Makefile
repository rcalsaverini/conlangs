LEXURGY := ../bin/lexurgy/bin/lexurgy sc
SOUND_CHANGES := lexurgy.lsc
WORDS_FILE := lexurgy.wli

watch:
	watchman-make -p '**/{*.lsc,*.wli}' -t run

.PHONY: run

run:
	$(LEXURGY) $(SOUND_CHANGES) $(WORDS_FILE)