
PYLINT_ERR_LEVEL=8
html_coverage_dir=.html
xml_coverage_file=coverage-report.xml
xml_report=test-results.xml
pip_install_dir=dist

all: test pylint coverage build

install_dev:
	$(MAKE) -C datastore install_dev
	$(MAKE) -C cmm install_dev
	$(MAKE) -C actsys install_dev
	$(MAKE) -C oobrestserver install_dev
	$(MAKE) -C oobrestclient install_dev

install:
	$(MAKE) -C datastore install
	$(MAKE) -C cmm install
	$(MAKE) -C actsys install
	$(MAKE) -C oobrestserver install
	$(MAKE) -C oobrestclient install

uninstall:
	$(MAKE) -C datastore uninstall
	$(MAKE) -C cmm uninstall
	$(MAKE) -C actsys uninstall
	$(MAKE) -C oobrestserver uninstall
	$(MAKE) -C oobrestclient uninstall

install_requirements:
	$(MAKE) -C datastore install_requirements
	$(MAKE) -C cmm install_requirements
	$(MAKE) -C actsys install_requirements
	$(MAKE) -C oobrestserver install_requirements
	$(MAKE) -C oobrestclient install_requirements

test: install_requirements
	$(MAKE) -C actsys test xml_report=$(xml_report)
	$(MAKE) -C datastore test xml_report=$(xml_report)
	$(MAKE) -C cmm test xml_report=$(xml_report)
	$(MAKE) -C oobrestserver test xml_report=$(xml_report)
	$(MAKE) -C oobrestclient test xml_report=$(xml_report)

pylint: install_requirements
	$(MAKE) -C actsys pylint PYLINT_ERR_LEVEL=$(PYLINT_ERR_LEVEL)
	$(MAKE) -C datastore pylint PYLINT_ERR_LEVEL=$(PYLINT_ERR_LEVEL)
	$(MAKE) -C cmm pylint PYLINT_ERR_LEVEL=$(PYLINT_ERR_LEVEL)
	$(MAKE) -C oobrestserver pylint PYLINT_ERR_LEVEL=$(PYLINT_ERR_LEVEL)
	$(MAKE) -C oobrestclient pylint PYLINT_ERR_LEVEL=$(PYLINT_ERR_LEVEL)

coverage: install_requirements
	$(MAKE) -C actsys coverage xml_coverage_file=$(xml_coverage_file) html_coverage_dir=$(html_coverage_dir)
	$(MAKE) -C datastore coverage xml_coverage_file=$(xml_coverage_file) html_coverage_dir=$(html_coverage_dir)
	$(MAKE) -C cmm coverage xml_coverage_file=$(xml_coverage_file) html_coverage_dir=$(html_coverage_dir)
	$(MAKE) -C oobrestserver coverage xml_coverage_file=$(xml_coverage_file) html_coverage_dir=$(html_coverage_dir)
	$(MAKE) -C oobrestclient coverage xml_coverage_file=$(xml_coverage_file) html_coverage_dir=$(html_coverage_dir)

rpm:
	$(MAKE) -C actsys rpm
	$(MAKE) -C datastore rpm
	$(MAKE) -C cmm rpm
	$(MAKE) -C oobrestserver rpm
	$(MAKE) -C oobrestclient rpm

build:
	$(MAKE) -C actsys build pip_install_dir=$(pip_install_dir)
	$(MAKE) -C datastore build pip_install_dir=$(pip_install_dir)
	$(MAKE) -C cmm build pip_install_dir=$(pip_install_dir)
	$(MAKE) -C oobrestserver build pip_install_dir=$(pip_install_dir)
	$(MAKE) -C oobrestclient build pip_install_dir=$(pip_install_dir)

dist: build
	-

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +
	find . -name $(xml_report) -exec rm --force {} +
	find . -name $(xml_coverage_file) -exec rm --force {} +
	$(MAKE) -C datastore clean
	$(MAKE) -C cmm clean
	$(MAKE) -C actsys clean
	$(MAKE) -C oobrestserver clean
	$(MAKE) -C oobrestclient clean

help:
	@echo "Supported actions are:"
	@echo "	build/dist"
	@echo "		Build this component and put a *.tar.gz, *.rpm and *.whl file in the dist folder."
	@echo "	test"
	@echo "		Run a all tests in this project."
	@echo "	pylint"
	@echo "		Run a pylint check."
	@echo "	coverage"
	@echo "		Perform a coverage analysis."
	@echo "	clean"
	@echo "		Clean all compiled files."

.PHONY: test pylint coverage clean rpm build dist
