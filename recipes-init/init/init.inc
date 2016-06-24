LICENSE = "CLOSED"
SECTION = "console/utils"

PR = "r0"

FILESEXTRAPATHS_append := "${THISDIR}/${PN}"
SRC_URI = "\
	file://${INIT_FILE} \
	"

S = "."

INITSCRIPT_NAME ?= "${INIT_FILE}"
INITSCRIPT_PARAMS ?= "start 99 5 . stop 99 0 1 6 ."

inherit update-rc.d

do_install() {
       install -d ${D}${sysconfdir}/init.d
       install -m 0755 ${WORKDIR}/${INIT_FILE} ${D}${sysconfdir}/init.d/${INIT_FILE}
}

FILES_${PN} = "${sysconfdir}/init.d/${INIT_FILE}"
