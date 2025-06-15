<script lang="ts">
	import TodoItem from './TodoItem.svelte';

	interface taskProps {
		taskName: string;
		isCompleted: boolean;
	}

	let task: string = $state('');
	let tasks: taskProps[] = $state([]);
	let mode = $state(0);

	function onclick() {
		let task_trim = task.trim();
		if (task_trim) {
			tasks.push({ taskName: task_trim, isCompleted: false });
		}
		task = '';
	}

	function onkeydown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			onclick();
		}
	}

	function toggleComplete(a_task: taskProps) {
		a_task.isCompleted = !a_task.isCompleted;
	}

	function toggleDeleteMode() {
		if (mode === 0) {
			mode = 1;
		} else {
			mode = 0;
		}
	}

	$inspect(tasks);
</script>

<div class="w-full flex flex-col items-center gap-3 justify-center p-4">
	<h1 class="font-semi text-2xl">Todo List</h1>

	<div class="flex flex-col gap-8 w-64">
		<div class="w-full bg-gray-100 p-3 shadow-xl rounded-xl grid grid-cols-2 gap-2">
			<input
				type="text"
				{onkeydown}
				bind:value={task}
				class="w-full border-2 border-black rounded-lg py-1 px-2 col-span-2"
				placeholder="Enter a task name..."
			/>
			<button class="bg-sky-200 p-2 rounded-lg" {onclick}>Add task</button>
			<button class="bg-red-200 p-2 rounded-lg" onclick={toggleDeleteMode}>Delete task</button>
		</div>

		<div class="flex flex-col gap-2">
			{#if mode === 0}
				{#each tasks as single_task}
					{#if !single_task.isCompleted}
						<button onclick={() => toggleComplete(single_task)}>
							<TodoItem name={single_task.taskName} completed={single_task.isCompleted} />
						</button>
					{/if}
				{/each}
				{#each tasks as single_task}
					{#if single_task.isCompleted}
						<button onclick={() => toggleComplete(single_task)}>
							<TodoItem name={single_task.taskName} completed={single_task.isCompleted} />
						</button>
					{/if}
				{/each}
			{:else}
				{#each tasks as single_task, index}
					{#if !single_task.isCompleted}
						<button onclick={() => toggleComplete(single_task)}>
							<TodoItem
								name={single_task.taskName}
								completed={single_task.isCompleted}
								mode={1}
								handleDelete={() => tasks.splice(index, 1)}
							/>
						</button>
					{/if}
				{/each}
				{#each tasks as single_task, index}
					{#if single_task.isCompleted}
						<button onclick={() => toggleComplete(single_task)}>
							<TodoItem
								name={single_task.taskName}
								completed={single_task.isCompleted}
								mode={1}
								handleDelete={() => tasks.splice(index, 1)}
							/>
						</button>
					{/if}
				{/each}
			{/if}
		</div>
	</div>
</div>
