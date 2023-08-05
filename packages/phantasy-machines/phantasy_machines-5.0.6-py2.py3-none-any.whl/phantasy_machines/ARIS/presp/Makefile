# read from xlsx
START_ELEM0 = "FS_PTG:PTA_D1000"
END_ELEM0 = "FS_F2S1:Q_D1476"

CONFIG = "phantasy.cfg"
OUT_LAYOUT = 'layout.csv'
OUT_CHANNELS = 'channels.csv'
LATTICE_TEMPLATE = 'template.lat'
SETTING_TEMPLATE = 'settings.json'

# read from layout.csv
START_ELEM = "FS_PTG:PTA_D1000"
END_ELEM = "FS_F1S2:VD_D1466"

PHYTOOL := python3 $(shell which phytool)

layout:
	$(PHYTOOL) frib-layout --cfg $(CONFIG) \
		--start $(START_ELEM0) \
		--end $(END_ELEM0) layout0.csv && \
	head -1 layout0.csv > $(OUT_LAYOUT) && \
	sed -n /$(START_ELEM)/,/$(END_ELEM)/p layout0.csv >> $(OUT_LAYOUT)
	rm layout0.csv

# mag
channels:
	$(PHYTOOL) frib-channels $(OUT_LAYOUT) $(OUT_CHANNELS) \
		--start $(START_ELEM) --end $(END_ELEM) \
		--pspvfile pspvconfig.csv \
		--tag 'F1'
	#--machine 'VA'

clean:
	rm $(OUT_LAYOUT) $(OUT_CHANNELS) layout0.csv

# 2 (after filling out SETTING_TEMPLATE)
flame_lattice:
	$(PHYTOOL) flame-lattice --config phantasy.cfg \
		--settings settings.json baseline.lat --mach ..

# 0 (if no settings file available)
lattice-template:
	$(PHYTOOL) flame-lattice $(LATTICE_TEMPLATE) \
		--layout $(OUT_LAYOUT) \
		--config $(CONFIG) \
		--mach .. \
		--start $(START_ELEM) \
		--end $(END_ELEM) \
		--template
# 1
settings-template:
	$(PHYTOOL) flame-settings $(LATTICE_TEMPLATE) $(SETTING_TEMPLATE) \
		--start "FS_F1S1:Q_D1013" \
		--end "FS_F1S2:SLV_D1463"

settings:
	$(PHYTOOL) flame-settings PSv08_v1.3test.lat settings.json \
		--start "FS_F1S1:Q_D1013" \
		--end "FS_F1S2:SLV_D1463"


.PHONY: layout channels clean
