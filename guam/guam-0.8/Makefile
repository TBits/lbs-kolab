REBAR = ./rebar #$(shell which rebar || echo ./rebar)
ENABLE_STATIC = no

all: deps-up guam

deps:
	$(REBAR) get-deps

deps-up: deps
	$(REBAR) update-deps

guam:
	ENABLE_STATIC=$(ENABLE_STATIC) $(REBAR) compile

run:
	erl -pa apps/*/ebin deps/*/ebin -config app -s kolab_guam

release:
	$(REBAR) compile generate

test.spec: test.spec.in cover.spec.in
	cat test.spec.in | sed -e "s,@PATH@,$(PWD)," > $(PWD)/test.spec
	cat cover.spec.in | sed -e "s,@PATH@,$(PWD)," > $(PWD)/cover.spec


test: test.spec guam
	mkdir -p test_logs
	ct_run -pa $(PWD)/apps/*/ebin -pa $(PWD)/deps/*/ebin -spec test.spec -erl_args -config $(PWD)/apps/kolab_guam/test/test.config -s kolab_guam
