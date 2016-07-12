FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"

SRC_URI += "file://99-usb-serial.rules"

do_install_append() {
    install -m 0644 ${WORKDIR}/99-usb-serial.rules ${D}${sysconfdir}/udev/rules.d/
}
