<script lang="ts">
	interface Props {
		name: string;
		completed?: boolean;
		mode?: number;
		handleDelete?: (id?: number) => void;
	}

	let { name, completed = false, mode = 0, handleDelete = () => {} }: Props = $props();
</script>

{#if mode === 0}
	<div
		class="flex w-full p-3 rounded-xl text-white text-lg font-bold {!completed
			? 'bg-sky-400'
			: 'bg-gray-400'}"
	>
		{name}
	</div>
{:else}
	<div
		class="flex w-full p-3 rounded-xl text-white text-lg font-bold {!completed
			? 'bg-sky-400'
			: 'bg-gray-400'}"
	>
		<span class="text-left w-[90%]">{name}</span>
		<button class="text-right w-[10%]" onclick={() => handleDelete()}>x</button>
	</div>
{/if}
