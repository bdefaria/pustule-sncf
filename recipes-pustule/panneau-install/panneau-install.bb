LICENSE="CLOSED"

PR = "r0"

S = "."

DEPENDS = "linux-yocto"

PACKAGES = "${PN}"
SRC_URI = "\
	   file://App.py \
	  "

FILES_${PN} = "/boot/zImage \
	       /boot/omap4-panda-es.dtb \
	       /home/root/App.py \
	       /home/root/raw \
	       /var/spool/sms/inbox \
	      "

do_install() {
	install -d ${D}/var
	install -d ${D}/var/spool
	install -d ${D}/var/spool/sms
	install -d ${D}/var/spool/sms/inbox
	install -d ${D}/home
	install -d ${D}/home/root
	install -d ${D}/home/root/raw
	install -d ${D}/boot
	install -m 0755 ${WORKDIR}/App.py ${D}/home/root/
	install -m 0755 ${DEPLOY_DIR_IMAGE}/zImage ${D}/boot/
	install -m 0755 ${DEPLOY_DIR_IMAGE}/zImage-omap4-panda-es.dtb ${D}/boot/omap4-panda-es.dtb
}
