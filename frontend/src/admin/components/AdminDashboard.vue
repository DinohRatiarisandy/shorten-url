<script lang="ts" setup>
import { onMounted, ref } from "vue";
import type { Link } from "@/types/link";
import { getAdminLinks } from "@/admin/services/admin.api.ts";

const API_URL = import.meta.env.VITE_API_URL;

const links = ref<Link[]>([]);
const loading = ref(false);
const error = ref("");

async function fetchLinks() {
    try {
        loading.value = true;
        error.value = ref("");
        links.value = await getAdminLinks();
    } catch (err) {
        error.value = err instanceof Error ? err.message : "unknown error";
    } finally {
        loading.value = false;
    }
}

onMounted(fetchLinks);
</script>
<template>
    <div
        class="relative overflow-x-auto bg-neutral-primary-soft shadow-xs rounded-base border border-default"
    >
        <table class="w-full text-sm text-left rtl:text-right text-body">
            <thead
                class="text-sm text-body bg-neutral-secondary-soft border-b rounded-base border-default"
            >
                <tr>
                    <th scope="col" class="px-6 py-3 font-medium">ID</th>
                    <th scope="col" class="px-6 py-3 font-medium">
                        Original URL
                    </th>
                    <th scope="col" class="px-6 py-3 font-medium">
                        Short Code
                    </th>
                    <th scope="col" class="px-6 py-3 font-medium">Created</th>
                    <th scope="col" class="px-6 py-3 font-medium">Action</th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="link in links"
                    :key="link.id"
                    class="bg-neutral-primary border-b border-default"
                >
                    <th
                        scope="row"
                        class="px-6 py-4 font-medium text-heading whitespace-nowrap"
                    >
                        {{ link.id }}
                    </th>
                    <td class="px-6 py-4">
                        <a
                            :href="link.original_url"
                            target="_blank"
                            class="text-blue-500"
                        >
                            {{ link.original_url }}
                        </a>
                    </td>
                    <td class="px-6 py-4">{{ link.short_code }}</td>
                    <td class="px-6 py-4">{{ link.created_at }}</td>
                    <td>
                        <button
                            class="flex items-center gap-1 px-3 py-1 text-sm text-white bg-red-500 rounded hover:bg-red-600 transition"
                        >
                            <span>Delete</span>
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
