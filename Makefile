.PHONY: test resources package install remove

test: resources
	plasmoidviewer .

resources: contents/code/images_rc.py
contents/code/images_rc.py: contents/code/images.qrc contents/images/*.svg
	cd contents/code; ./makeResources.sh

package: resources
	@echo -e "\n[PACKAGE]"
	zip -x Makefile -x nvtemp.zip -r /tmp/nvtemp.zip .
	mv /tmp/nvtemp.zip .

install: package
	AUX=$(plasmapkg -l | grep "NVidia-DualMonitor-Control"); if [ ! -z "$AUX" ]; then $(MAKE) --no-print-directory remove; fi
	@echo -e "\n[INSTALL]"
	plasmapkg -i nvtemp.zip

remove:
	@echo -e "\n[REMOVE]"
	plasmapkg -r "NVidia-DualMonitor-Control"
