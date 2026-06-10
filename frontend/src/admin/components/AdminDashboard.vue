<script lang="ts" setup>
import { onMounted, ref } from "vue";
import type { Link } from "@/types/link";
import {
    getAdminLinks,
    deleteAdminLink,
    logoutAdmin,
} from "@/admin/services/admin.api.ts";
import { useRouter } from "vue-router";

const API_URL = import.meta.env.VITE_API_URL;
const router = useRouter();

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

async function deleteLink(id: number) {
    try {
        await deleteAdminLink(id);

        links.value = links.value.filter((l) => l.id !== id);
    } catch (err) {
        error.value = err instanceof Error ? err.message : "delete failed";
    }
}

async function logout() {
    try {
        await logoutAdmin();
        localStorage.clear();
        router.push("/admin/login");
    } catch (err) {
        error.value = err instanceof Error ? err.message : "Error when logout";
    }
}

onMounted(fetchLinks);
</script>
<template>
    <button
        @click="logout"
        class="mx-2 my-2 px-4 py-2 bg-gray-800 text-white rounded hover:bg-gray-700"
    >
        Logout
    </button>
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
                            @click="deleteLink(link.id)"
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
