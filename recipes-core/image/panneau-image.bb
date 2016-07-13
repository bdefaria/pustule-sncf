SUMMARY = "A small image just capable of allowing a device to boot."

IMAGE_INSTALL = "packagegroup-core-boot \
		 ${CORE_IMAGE_EXTRA_INSTALL} \
		 ${ROOTFS_PKGMANAGE_BOOTSTRAP} \
		 App-init \
		 gammu \
		 gammu-init \
		 gammu-smsd \
		 panneau-install \
		 python3 \
		 python3-importlib \
		 python3-misc \
		 python3-pyserial \
		 python3-textutils \
		 udev-extraconf \
		 usb-modeswitch \
		 usbutils \
		 "

LICENSE = "MIT"

inherit core-image

IMAGE_ROOTFS_SIZE ?= "8192"
IMAGE_ROOTFS_EXTRA_SPACE_append = "${@bb.utils.contains("DISTRO_FEATURES", "systemd", " + 4096", "" ,d)}"
inherit extrausers
EXTRA_USERS_PARAMS = "usermod -P nl09 root;"
IMAGE_LINGUAS = "fr-fr"
