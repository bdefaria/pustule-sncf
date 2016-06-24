LICENSE="CLOSED"

PR = "r0"

S = "."

DEPENDS = "linux-yocto"

PACKAGES = "${PN}"
FILES_${PN} = "/boot/zImage \
	       /boot/omap4-panda-es.dtb \
	       /var/spool/sms \
	      "

do_install() {
	install -d ${D}/var
	install -d ${D}/var/spool
	install -d ${D}/var/spool/sms
	install -d ${D}/boot
	install -m 0755 ${DEPLOY_DIR_IMAGE}/zImage ${D}/boot/
	install -m 0755 ${DEPLOY_DIR_IMAGE}/zImage-omap4-panda-es.dtb ${D}/boot/omap4-panda-es.dtb
}
