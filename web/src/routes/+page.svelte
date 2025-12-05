<script lang="ts">
	import { tick } from 'svelte';

	type LogEntry = { prefix: string; text: string };

	const starterLogs: LogEntry[] = [
		{ prefix: 'BOOT', text: 'Gridlines calibrated.' },
		{ prefix: 'AGENT/K0R', text: 'Awaiting directives.' }
	];

	let logs: LogEntry[] = [...starterLogs];
	let prompt = '';
	let logPane: HTMLDivElement | null = null;
	let sending = false;

	const addLog = (entry: LogEntry) => {
		logs = [...logs, entry];
	};

	const scrollLog = async () => {
		await tick();
		if (logPane) {
			logPane.scrollTop = logPane.scrollHeight;
		}
	};

	const sendPrompt = async () => {
		const value = prompt.trim();
		if (!value || sending) return;
		sending = true;
		addLog({ prefix: 'USER', text: value });
		prompt = '';
		scrollLog();

		try {
			const res = await fetch('/api/ask', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ prompt: value })
			});
			const data = await res.json();
			addLog({ prefix: 'AGENT/K0R', text: data?.reply ?? 'Stub response.' });
		} catch (err) {
			addLog({ prefix: 'AGENT/K0R', text: 'Link backend to LLM. Stub in use.' });
			console.error(err);
		} finally {
			sending = false;
			scrollLog();
		}
	};

	const onSubmit = (event: SubmitEvent) => {
		event.preventDefault();
		void sendPrompt();
	};
</script>

<svelte:head>
	<link
		rel="preconnect"
		href="https://fonts.googleapis.com"
	/>
	<link
		rel="preconnect"
		href="https://fonts.gstatic.com"
		crossorigin
	/>
	<link
		href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Manrope:wght@400;600&display=swap"
		rel="stylesheet"
	/>
	<title>KL1KK0 — Amber Grid</title>
</svelte:head>

<div class="page">
	<header>
		<div class="brand">
			<span>KL1KK0</span>
			<div>Custom AI for the Unsolved</div>
		</div>
		<div class="cmd-bar">KL1KK0://amber-grid-greenfocus — green prompts</div>
	</header>

	<aside class="left">
		<form class="prompt" on:submit={onSubmit}>
			<label for="prompt">>_</label>
			<input
				id="prompt"
				name="prompt"
				type="text"
				placeholder="Ask KL1KK0 anything..."
				bind:value={prompt}
				autocomplete="off"
			/>
			<button type="submit" aria-label="Run prompt">run</button>
		</form>
		<div class="log" bind:this={logPane} aria-live="polite">
			{#each logs as entry}
				<div class="log-line">
					<strong
						><span class="bracket">[</span>{entry.prefix}<span class="bracket">]</span></strong
					>
					<span>{entry.text}</span>
				</div>
			{/each}
		</div>
	</aside>

	<main class="right">
		<section class="module">
			<div class="badge">/identity</div>
			<h3>Built to click. Born to question.</h3>
			<p>
				KL1KK0 is a boutique AI research and engineering studio. We build bespoke agents,
				architectures, and systems for teams operating beyond template solutions.
			</p>
		</section>
		<section class="module">
			<div class="badge">/agents</div>
			<h3>Custom Agents</h3>
			<p>
				Domain-specific collaborators with long-term memory, adaptive reasoning, workflow
				orchestration, and multi-agent coordination.
			</p>
		</section>
		<section class="module">
			<div class="badge">/products</div>
			<h3>High-End AI Product Development</h3>
			<p>
				Complete AI-driven products, proprietary inference pipelines, and specialized interfaces
				tuned to your domain.
			</p>
		</section>
		<section class="module">
			<div class="badge">/research</div>
			<h3>Independent Research</h3>
			<p>
				Cognitive architectures, memory systems, symbolic+neural hybrids, agent planning, and novel
				interface paradigms.
			</p>
		</section>
		<section class="module">
			<div class="badge">/sprites</div>
			<h3>Terminal Sprites</h3>
			<p>
				Identity-layer archetypes representing core agent behaviors: K0R (analysis), L1T
				(exploration), KIK (synthesis), O0N (continuity).
			</p>
		</section>
		<section class="module">
			<div class="badge">/process</div>
			<h3>Process</h3>
			<p>
				Discovery → Prototype → Refinement → Deployment → Evolution. Precision engineering with
				long-term collaboration.
			</p>
			<div class="cta">
				<button type="button">&gt; start_project</button>
				<button type="button">&gt; request_consultation</button>
				<button type="button">&gt; view_capabilities</button>
			</div>
		</section>
	</main>

	<footer>
		<div>KL1KK0/AMBER-GRID-GREENFOCUS/READY · MEMORY: ACTIVE · USER: CONNECTED</div>
		<div>v0.1 amber-grid-greenfocus</div>
	</footer>
</div>

<style>
	:global(:root) {
		color-scheme: dark;
	}
	:global(*) {
		box-sizing: border-box;
	}
	:global(body) {
		margin: 0;
		background: var(--bg);
		color: var(--text);
		font-family: 'Manrope', system-ui, sans-serif;
		min-height: 100vh;
	}
	.page {
		display: grid;
		grid-template-columns: 34% 66%;
		min-height: 100vh;
		background: var(--bg);
		color: var(--text);
		font-family: 'Manrope', system-ui, sans-serif;
		--bg: #0c0a06;
		--panel: #15100c;
		--border: #3a2d1c;
		--border-bright: #4c3a23;
		--amber: #ffb547;
		--green: #6dff72;
		--text: #f4e9d6;
		--sub: #bca987;
		--glow: 0 0 18px rgba(255, 181, 71, 0.2);
		background-image: linear-gradient(rgba(255, 181, 71, 0.03) 1px, transparent 1px),
			linear-gradient(90deg, rgba(255, 181, 71, 0.03) 1px, transparent 1px);
		background-size: 28px 28px;
	}
	header {
		grid-column: 1 / -1;
		padding: 16px 22px;
		border-bottom: 1px solid var(--border);
		background: linear-gradient(90deg, rgba(255, 181, 71, 0.08), rgba(255, 181, 71, 0.02));
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
		font-family: 'JetBrains Mono', monospace;
		letter-spacing: 0.03em;
	}
	.brand {
		display: flex;
		align-items: center;
		gap: 12px;
	}
	.brand span {
		display: inline-block;
		padding: 6px 10px;
		border: 1px solid var(--border-bright);
		background: #0f0c09;
		box-shadow: var(--glow);
	}
	.cmd-bar {
		color: var(--amber);
		font-size: 14px;
	}
	.left {
		border-right: 1px solid var(--border-bright);
		padding: 18px 16px;
		background: radial-gradient(circle at 32% 22%, rgba(255, 181, 71, 0.08), transparent 44%);
		display: flex;
		flex-direction: column;
		gap: 14px;
	}
	.prompt,
	.log {
		border: 1px dashed var(--border-bright);
		background: #0f0c09;
		font-family: 'JetBrains Mono', monospace;
	}
	.prompt {
		display: flex;
		align-items: center;
		gap: 8px;
		padding: 10px 12px;
	}
	.prompt label {
		color: var(--text);
	}
	.prompt input {
		flex: 1;
		background: transparent;
		border: none;
		color: var(--green);
		font-size: 15px;
		outline: none;
		caret-color: var(--green);
	}
	.prompt button {
		padding: 6px 12px;
		background: transparent;
		border: 1px solid var(--border-bright);
		color: var(--amber);
		font-weight: 700;
		cursor: pointer;
		text-transform: lowercase;
	}
	.prompt button:hover {
		border-color: var(--green);
		color: var(--text);
	}
	.log {
		flex: 1;
		padding: 14px;
		box-shadow: inset 0 0 0 1px #0a0806;
		overflow-y: auto;
		max-height: calc(100vh - 160px);
		color: var(--sub);
	}
	.log-line {
		margin: 4px 0;
		display: flex;
		gap: 8px;
	}
	.log-line strong {
		color: var(--green);
		font-weight: 600;
	}
	.bracket {
		color: var(--amber);
	}
	.right {
		padding: 22px;
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
		gap: 16px;
	}
	.module {
		border: 1px dashed var(--border);
		background: var(--panel);
		padding: 16px;
		position: relative;
		overflow: hidden;
		box-shadow: var(--glow);
	}
	.module::before {
		content: '';
		position: absolute;
		inset: 0;
		background: linear-gradient(135deg, rgba(112, 255, 119, 0.08), rgba(255, 181, 71, 0.06));
		opacity: 0;
		transition: opacity 160ms ease;
	}
	.module:hover::before {
		opacity: 0.2;
	}
	.module h3 {
		margin: 0 0 8px;
		font-family: 'JetBrains Mono', monospace;
		letter-spacing: 0.02em;
	}
	.module p {
		margin: 0 0 10px;
		color: var(--sub);
		line-height: 1.4;
	}
	.badge {
		display: inline-flex;
		align-items: center;
		gap: 6px;
		padding: 4px 8px;
		border: 1px dashed var(--border-bright);
		color: var(--green);
		font-family: 'JetBrains Mono', monospace;
		font-size: 12px;
		margin-bottom: 10px;
	}
	.cta {
		display: inline-flex;
		gap: 8px;
		flex-wrap: wrap;
	}
	.cta button {
		background: transparent;
		color: var(--green);
		border: 1px dashed var(--border-bright);
		padding: 8px 12px;
		font-family: 'JetBrains Mono', monospace;
		cursor: pointer;
	}
	.cta button:hover {
		border-color: var(--green);
		color: var(--text);
	}
	footer {
		grid-column: 1 / -1;
		border-top: 1px solid var(--border);
		padding: 10px 16px;
		font-family: 'JetBrains Mono', monospace;
		color: var(--sub);
		background: #0f0c09;
		display: flex;
		justify-content: space-between;
	}
	@media (max-width: 900px) {
		.page {
			grid-template-columns: 1fr;
		}
		.left {
			max-height: 38vh;
		}
		.log {
			max-height: 26vh;
		}
	}
</style>
