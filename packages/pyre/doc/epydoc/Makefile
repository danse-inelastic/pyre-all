PKGNAME = pyre
OUTPUT = html
WEBDOCDIR = login.cacr.caltech.edu:/cacr/home/proj/danse/docs.danse.us/docroot/pyre


all:
	epydoc --config=epydoc.cfg --output=$(OUTPUT) \
	       --name=$(PKGNAME) $(PKGNAME)


clean:
	/bin/rm -rf $(OUTPUT)


publish:
	rsync -e /usr/bin/ssh -va --chmod=a+rwx,o-w,Dg+s,Fa-x \
	    $(OUTPUT)/ $(WEBDOCDIR)/$(PKGNAME)