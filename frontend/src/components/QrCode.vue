<script setup>
import { ref, watch } from "vue";
import QRCode from "qrcode";

const props = defineProps({
	url: String,
});

const qrImage = ref("");

const generateQR = async (value) => {
	if (!value) return;

	qrImage.value = await QRCode.toDataURL(value, {
		width: 200,
		margin: 2,
	});
};

watch(
	() => props.url,
	(newVal) => {
		generateQR(newVal);
	},
	{ immediate: true },
);
</script>

<template>
	<div v-if="qrImage">
		<img :src="qrImage" alt="QR Code" />
	</div>
</template>
