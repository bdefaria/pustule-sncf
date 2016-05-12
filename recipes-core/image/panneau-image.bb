SUMMARY = "A small image just capable of allowing a device to boot."

IMAGE_INSTALL = "${CORE_IMAGE_EXTRA_INSTALL} \
		 ${ROOTFS_PKGMANAGE_BOOTSTRAP} \
		 "

LICENSE = "MIT"

inherit core-image
