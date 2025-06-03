<script>
	import { fade } from 'svelte/transition';
	import Tabela from '$lib/components/tabela.svelte';
	const API_URL = 'http://localhost:3333/';

	let playerHP = 8;
	let opponentHP = 8;
	let roundWins = { player: 0, ai: 0 };
	let matchWins = { player: 0, ai: 0 };
	let resultMsg = '';
	let showTableModal = false;
	let isDefending = false;
	let showGameEndModal = false;
	let gameEndMessage = '';

	// Variáveis para animações
	let shakePlayer = false;
	let shakeOpponent = false;
	let pulseVictory = false;
	let screenShake = false;
	const maxHP = 8;

	// Variáveis para personagens
	let playerHit = false;
	let opponentHit = false;
	let playerSprite = 'default';
	let opponentSprite = 'default';

	let table = [
		[1, 0, 1, 0, -1.4, 1, 1],
		[0, 3.5, -3.5, -1, 3, -3.5, 3.5],
		[0, 0, 3.5, 3.5, -1.4, -3.5, 3.5],
		[0, 0, 2.5, 2.5, -1.4, 2.5, -3.5],
		[0, 0, -3, 3, 3.5, 0, 0]
	];

	const defensiveOptions = [
		'Defender',
		'Guard-jump',
		'Botão',
		'Agarrão',
		'Reversal',
		'Parry Alto',
		'Parry Baixo'
	];

	const offensiveOptions = ['Agarrão', 'Combo com Atraso', 'Meaty Alto', 'Meaty Baixo', 'Shimmy'];

	const defensiveOptionsButtonText = [
		['Defender', 'Vence Combo c/ Atraso, Meaty e Shimmy'],
		['Guard-jump', 'Vence Agarrão, Meaty e Shimmy'],
		['Botão', 'Vence Shimmy(3), Combo com Atraso(3.5)'],
		['Agarrão', 'Vence Combo c/ Atraso(1)'],
		['Reversal', 'Vence Agarrão e Meaty, com 1.4 de dano'],
		['Parry Alto', 'Vence Combo c/ Atraso e Meaty Alto, com 3.5 de dano'],
		['Parry Baixo', 'Vence Meaty baixo (3.5)']
	];

	const offensiveOptionsButtonText = [
		['Agarrão', 'Vence Defender, Botão e Parry (1 de dano)'],
		['Combo com Atraso', 'Vence Guard-Jump(3.5), Parry Baixo(3.5) e Reversal(3)'],
		['Meaty Alto', 'Vence Agarrão, Parry Baixo, botão, com 3.5 de dano'],
		['Meaty Baixo', 'Vence Agarrão, Parry alto e botão, com 2.5 de dano'],
		['Shimmy', 'Vence Agarrão(3) e Reversal(3.5)']
	];

	let lastChoices = {
		player: '',
		opponent: '',
		outcome: ''
	};

	// Opções de música
	const musicOptions = [
		{
			name: "Makoto's Stage - Spunky",
			url: 'https://soundcloud.com/user-262249214/street-fighter-iii-3rd-strike-makotos-stage-spunky-original'
		},
		{
			name: "Akuma's Stage - Killing Moon",
			url: 'https://soundcloud.com/menino-garoto/street-fighter-iii-3rd-strike-akumas-stage-killing-moon'
		},
		{
			name: 'Alex/Ken Theme',
			url: 'https://soundcloud.com/menino-garoto/alex-ken-theme-hd'
		},
		{
			name: "Gill's Stage - Psyche Out",
			url: 'https://soundcloud.com/menino-garoto/street-fighter-iii-3rd-strike-gills-stage-psyche-out'
		},
		{
			name: "Remy's Stage - The Beep",
			url: 'https://soundcloud.com/menino-garoto/street-fighter-iii-3rd-strike-remys-stage-the-beep'
		}
	];

	// Função para abrir música em nova aba
	function openMusicInNewTab(url) {
		window.open(url, '_blank');
	}

	async function play(playerChoice, defense) {
		// Reset animações
		shakePlayer = false;
		shakeOpponent = false;
		pulseVictory = false;
		playerHit = false;
		opponentHit = false;
		screenShake = false;

		try {
			let response, data;
			let opponentChoice;
			let damage;

			if (defense) {
				// Jogador está se defendendo → oponente ataca → pegar ação ofensiva
				response = await fetch(`${API_URL}/offense`);
				data = await response.json();
				opponentChoice = data.action;

				damage = parseFloat(table[opponentChoice][playerChoice].toFixed(1));

				lastChoices.player = defensiveOptions[playerChoice];
				lastChoices.opponent = offensiveOptions[opponentChoice];

				if (damage > 0) {
					playerHP = parseFloat((playerHP - damage).toFixed(1));
					resultMsg = `Você foi acertado! Sofreu ${damage} de dano.`;
					lastChoices.outcome = 'O oponente venceu a interação.';
					shakePlayer = true;
					screenShake = true;
					playerHit = true;
					playerSprite = 'defending';
					opponentSprite = 'attack';
					isDefending = true;
				} else if (damage < 0) {
					opponentHP = parseFloat((opponentHP + damage).toFixed(1));
					resultMsg = `Você venceu a interação! Causou ${-damage} de dano.`;
					lastChoices.outcome = 'Você venceu a interação.';
					shakeOpponent = true;
					opponentHit = true;
					playerSprite = 'attack';
					opponentSprite = 'defending';
					isDefending = false;
					resultMsg += ' Você ganhou a vantagem e agora ataca!';
				} else {
					resultMsg = 'Empate! Nenhum dano causado.';
					lastChoices.outcome = 'Empate na troca.';
					isDefending = Math.floor(Math.random() * 2) === 0;
					if (!isDefending) {
						resultMsg += ' Você ganhou a vantagem e agora ataca!';
						playerSprite = 'attack';
						opponentSprite = 'defending';
					} else {
						resultMsg += ' O oponente mantém a vantagem.';
						playerSprite = 'defending';
						opponentSprite = 'attack';
					}
				}
			} else {
				// Jogador está atacando → oponente defende → pegar ação defensiva
				response = await fetch(`${API_URL}/defense`);
				data = await response.json();
				opponentChoice = data.action;

				damage = parseFloat(table[playerChoice][opponentChoice].toFixed(1));

				lastChoices.player = offensiveOptions[playerChoice];
				lastChoices.opponent = defensiveOptions[opponentChoice];

				if (damage > 0) {
					opponentHP = parseFloat((opponentHP - damage).toFixed(1));
					resultMsg = `Você acertou! Causou ${damage} de dano.`;
					lastChoices.outcome = 'Você venceu a interação.';
					shakeOpponent = true;
					opponentHit = true;
					playerSprite = 'attack';
					opponentSprite = 'defending';
					isDefending = false;
				} else if (damage < 0) {
					playerHP = parseFloat((playerHP + damage).toFixed(1));
					resultMsg = `Você perdeu a interação! Sofreu ${-damage} de dano.`;
					lastChoices.outcome = 'O oponente venceu a interação.';
					shakePlayer = true;
					screenShake = true;
					playerHit = true;
					playerSprite = 'defending';
					opponentSprite = 'attack';
					isDefending = true;
				} else {
					resultMsg = 'Empate! Nenhum dano causado.';
					lastChoices.outcome = 'Empate na troca.';
					isDefending = Math.floor(Math.random() * 2) === 0;
					if (isDefending) {
						resultMsg += ' O oponente ganhou a vantagem e agora ataca!';
						playerSprite = 'defending';
						opponentSprite = 'attack';
					} else {
						playerSprite = 'ready';
						resultMsg += ' Você mantém a vantagem.';
						playerSprite = 'attack';
						opponentSprite = 'defending';
					}
				}
			}

			checkRound(playerChoice);
		} catch (error) {
			console.error('Erro na comunicação com o servidor:', error);
			resultMsg = 'Erro ao tentar se comunicar com o servidor.';
		}
	}

	async function checkRound(playerChoice) {
		let winner = null;
		let roundEnded = false;

		if (playerHP <= 0) {
			roundWins.ai++;
			winner = 'ai';
			isDefending = true;
			resultMsg = 'Novo round! Fight!';
			resetRound();
			roundEnded = true;
		} else if (opponentHP <= 0) {
			roundWins.player++;
			winner = 'player';
			resultMsg = 'Novo round! Fight!';
			resetRound();
			roundEnded = true;
		}

		const roundNumber = roundWins.player + roundWins.ai;

		try {
			await fetch(`${API_URL}/update`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					event: 'round_update',
					action: playerChoice,
					round: roundNumber,
					winner: winner, // será null se o round não terminou
					roundWins: { ...roundWins },
					matchWins: { ...matchWins }
				})
			});
		} catch (error) {
			console.error('Erro ao enviar dados de update:', error);
		}

		// Checar se alguém venceu a partida
		if (roundEnded) {
			if (roundWins.player === 2) {
				matchWins.player++;
				resultMsg = `Você venceu a partida! O placar é: ${matchWins.player}:${matchWins.ai}`;
				resetMatch();
			} else if (roundWins.ai === 2) {
				matchWins.ai++;
				resultMsg = `Você perdeu a partida! O placar é: ${matchWins.player}:${matchWins.ai}`;
				isDefending = false;
				resetMatch();
			}
		}
	}

	function resetRound() {
		playerHP = 8;
		opponentHP = 8;
		playerSprite = 'default';
		opponentSprite = 'default';
	}

	function resetMatch() {
		playerHP = 8;
		opponentHP = 8;
		roundWins.player = 0;
		roundWins.ai = 0;
		playerSprite = 'default';
		opponentSprite = 'default';

		// Verificar se alguém chegou a 10 vitórias
		if (matchWins.player === 10) {
			gameEndMessage =
				'Você ganhou! Parabéns. Você pode fechar este modal e continuar jogando se quiser, mas já temos os dados que precisamos. Muito obrigado por jogar!';
			showGameEndModal = true;
		} else if (matchWins.ai === 10) {
			gameEndMessage =
				'Você perdeu! Que pena. Você pode fechar este modal e continuar jogando se quiser, mas já temos os dados que precisamos. Muito obrigado por jogar!';
			showGameEndModal = true;
		}
	}
</script>

<!-- Container principal com tamanho fixo -->
<div class="fixed-container">
	<div class="bg flex min-h-screen items-center justify-center p-4">
		<!-- Placar de partidas no topo -->
		<div
			class="absolute -top-0 left-1/2 w-[410px] -translate-x-1/2 transform rounded-lg bg-gray-800 px-6 py-3 text-2xl font-bold text-yellow-100 shadow-lg"
		>
			Partidas: Você {matchWins.player} × {matchWins.ai} Oponente
		</div>
		<!-- Cardbox central com tamanho fixo -->
		<div
			class="game-card relative h-[100vh] w-[90vw] rounded-2xl bg-black/90 p-8 text-white shadow-2xl {screenShake
				? 'animate-screen-shake'
				: ''}"
		>
			<!-- Botão Tabela e Música -->
			<div class="absolute right-4 top-4 flex gap-2">
				<button
					class="flex items-center gap-2 rounded-lg bg-gray-700 px-4 py-2 text-white transition hover:bg-gray-600"
					on:click={() => (showTableModal = true)}
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-6 w-6"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M4 6h16M4 10h16M4 14h16M4 18h16"
						/>
					</svg>
					<span>Tabela</span>
				</button>

				<!-- Menu de Música -->
				<div class="relative">
					<button
						class="flex items-center gap-2 rounded-lg bg-gray-700 px-4 py-2 text-white transition hover:bg-gray-600"
						on:click={() => document.getElementById('musicDropdown').classList.toggle('hidden')}
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-6 w-6"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3"
							/>
						</svg>
						<span>Música</span>
					</button>

					<div
						id="musicDropdown"
						class="absolute right-0 z-10 mt-2 hidden w-64 rounded-lg bg-gray-800 shadow-lg"
					>
						<div class="p-2">
							{#each musicOptions as track}
								<button
									on:click={() => openMusicInNewTab(track.url)}
									class="block w-full rounded px-4 py-2 text-left hover:bg-gray-700"
								>
									{track.name}
								</button>
							{/each}
						</div>
					</div>
				</div>
			</div>

			<!-- Cabeçalho -->
			<h1 class="font-orbitron mb-8 text-center text-5xl font-bold tracking-wide text-yellow-400">
				OKIZEME SHOWDOWN
			</h1>

			<!-- Área de combate -->
			<div class="mb-8 flex items-end justify-between">
				<!-- Jogador -->
				<div class="flex w-[45%] flex-col items-center">
					<!-- Personagem do Jogador -->
					<div
						class="relative mb-2 h-32 w-32 transition-all duration-300 {playerHit
							? 'animate-hit'
							: ''}"
					>
						{#if playerSprite === 'defending'}
							<img
								src="https://wiki.supercombo.gg/images/a/a4/%28kenhparry%29.gif"
								alt="Player defending"
								class="w-fullobject-contain slow-gif h-full"
							/>
						{:else if playerSprite === 'attack'}
							<img
								src="https://wiki.supercombo.gg/images/a/ae/%28kencmp%29.gif"
								alt="Player Attack"
								class="slow-gif h-full w-full object-contain"
							/>
						{:else if playerSprite === 'ready'}
							<img
								src="http://ensabahnur.free.fr/BastonNew/ImagesCharacters/ken-stance.gif"
								alt="Player Ready"
								class="slow-gif h-full w-full object-contain brightness-125 contrast-125"
							/>
						{:else}
							<img
								src="http://ensabahnur.free.fr/BastonNew/ImagesCharacters/ken-stance.gif"
								alt="Player Default"
								class="slow-gif h-full w-full object-contain"
							/>
						{/if}
					</div>

					<div class="mb-2 text-2xl font-bold text-blue-400">JOGADOR</div>
					<div class="relative h-8 w-full rounded-full bg-gray-700 shadow-inner">
						<div
							class="h-full rounded-full bg-gradient-to-r from-blue-500 to-blue-600 transition-all duration-500 ease-out"
							class:shake={shakePlayer}
							style={`width: ${(playerHP / maxHP) * 100}%`}
						></div>
						<div
							class="absolute inset-0 flex items-center justify-center text-sm font-bold text-white"
						>
							{playerHP.toFixed(1)} HP
						</div>
					</div>
				</div>

				<!-- VS -->
				<div class="mx-4 flex flex-col items-center p-4">
					<div class="mt-2 w-[210px] pb-2 text-3xl font-semibold">
						Rounds: {roundWins.player} × {roundWins.ai}
					</div>
					<div class="text-4xl font-bold text-red-500">VS</div>
				</div>

				<!-- Oponente -->
				<div class="flex w-[45%] flex-col items-center">
					<!-- Personagem do Oponente -->
					<div
						class="relative mb-2 h-32 w-32 transition-all duration-300 {opponentHit
							? 'animate-hit'
							: ''}"
					>
						{#if opponentSprite === 'defending'}
							<img
								src="https://wiki.supercombo.gg/images/a/a4/%28kenhparry%29.gif"
								alt="Opponent defending"
								class="slow-gif h-full w-full scale-x-[-1] transform object-contain"
								style="filter: hue-rotate(180deg) saturate(1.2);"
							/>
						{:else if opponentSprite === 'attack'}
							<img
								src="https://wiki.supercombo.gg/images/a/ae/%28kencmp%29.gif"
								alt="Opponent Attack"
								class="slow-gif h-full w-full scale-x-[-1] transform object-contain"
								style="filter: hue-rotate(180deg) saturate(1.2);"
							/>
						{:else if opponentSprite === 'ready'}
							<img
								src="http://ensabahnur.free.fr/BastonNew/ImagesCharacters/ken-stance.gif"
								alt="Opponent Ready"
								class="slow-gif h-full w-full scale-x-[-1] transform object-contain brightness-125 contrast-125"
								style="filter: hue-rotate(180deg) saturate(1.2);"
							/>
						{:else}
							<img
								src="http://ensabahnur.free.fr/BastonNew/ImagesCharacters/ken-stance.gif"
								alt="Opponent Default"
								class="slow-gif h-full w-full scale-x-[-1] transform object-contain"
								style="filter: hue-rotate(180deg) saturate(1.2);"
							/>
						{/if}
					</div>

					<div class="mb-2 text-2xl font-bold text-red-400">OPONENTE</div>
					<div class="relative h-8 w-full rounded-full bg-gray-700 shadow-inner">
						<div
							class="h-full rounded-full bg-gradient-to-r from-red-500 to-red-600 transition-all duration-500 ease-out"
							class:shake={shakeOpponent}
							style={`width: ${(opponentHP / maxHP) * 100}%`}
						></div>
						<div
							class="absolute inset-0 flex items-center justify-center text-sm font-bold text-white"
						>
							{opponentHP.toFixed(1)} HP
						</div>
					</div>
				</div>
			</div>

			<!-- Modo de jogo atual -->
			<h2 class="mb-6 text-center text-2xl font-semibold text-gray-300">
				{isDefending ? 'ESCOLHA SUA DEFESA' : 'ESCOLHA SEU ATAQUE'}
			</h2>

			<!-- Ações -->
			<div class="mb-8 grid h-[360px] grid-cols-2 gap-4">
				{#if isDefending}
					{#each defensiveOptionsButtonText as [title, description], index}
						<button
							on:click={() => play(index, true)}
							class="flex flex-col items-start justify-start rounded-xl border-2 border-blue-400 bg-blue-600/80 p-4 text-left transition hover:bg-blue-700/90 hover:shadow-lg hover:shadow-blue-500/20 active:scale-95 active:bg-blue-800"
						>
							<span class="text-xl font-semibold">{title}</span>
							<span class="text-md opacity-80">{description}</span>
						</button>
					{/each}
				{:else}
					{#each offensiveOptionsButtonText as [title, description], index}
						<button
							on:click={() => play(index, false)}
							class="flex flex-col items-start justify-start rounded-xl border-2 border-red-400 bg-red-600/80 p-4 text-left transition hover:bg-red-700/90 hover:shadow-lg hover:shadow-red-500/20 active:scale-95 active:bg-red-800"
						>
							<span class="text-xl font-semibold">{title}</span>
							<span class="text-md opacity-80">{description}</span>
						</button>
					{/each}
				{/if}
			</div>

			<!-- Resultado da jogada -->
			<div class="rounded-lg bg-gray-800/50 p-4 text-center" transition:fade>
				{#if lastChoices.player}
					<div class="grid grid-cols-3 gap-4 text-lg">
						<div class="text-right text-blue-400">
							<div class="font-bold">Você</div>
							<div class="text-3xl font-semibold">{lastChoices.player}</div>
							<!-- Texto maior e semibold -->
						</div>
						<div class="flex items-center justify-center text-2xl">
							<div class="rounded-full bg-gray-700 p-2">⚔️</div>
						</div>
						<div class="text-left text-red-400">
							<div class="font-bold">Oponente</div>
							<div class="text-3xl font-semibold">{lastChoices.opponent}</div>
							<!-- Texto maior e semibold -->
						</div>
					</div>
					<div class="mt-2 text-xl font-semibold text-yellow-300">{lastChoices.outcome}</div>
				{/if}
				<p class="mt-3 animate-bounce text-2xl font-bold">{resultMsg}</p>
			</div>
		</div>

		<!-- Modal da Tabela -->
		{#if showTableModal}
			<div
				class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm"
				role="dialog"
				aria-modal="true"
				tabindex="-1"
				on:keydown={(e) => (e.key === 'Escape' ? (showTableModal = false) : null)}
				on:click={() => (showTableModal = false)}
				transition:fade
			>
				<div
					class="relative w-[60%] overflow-auto rounded-2xl bg-gray-800 p-6 text-white shadow-2xl"
					on:click|stopPropagation
				>
					<button
						on:click={() => (showTableModal = false)}
						class="absolute right-4 top-4 rounded-full bg-gray-700 p-2 text-white hover:bg-gray-600"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="h-6 w-6"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
						>
							<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
					<Tabela />
				</div>
			</div>
		{/if}
	</div>

	<!-- Modal de Fim de Jogo (10 partidas) -->
	{#if showGameEndModal}
		<div
			class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
			role="dialog"
			aria-modal="true"
			transition:fade
		>
			<div
				class="relative max-w-md rounded-2xl border-2 border-yellow-400 bg-gray-800 p-8 text-white shadow-2xl"
			>
				<div class="text-center">
					<div class="mb-4 text-3xl">🎉</div>
					<h2 class="mb-4 text-2xl font-bold text-yellow-400">Fim de Jogo!</h2>
					<p class="mb-6 text-lg leading-relaxed">{gameEndMessage}</p>
					<button
						on:click={() => (showGameEndModal = false)}
						class="rounded-lg bg-yellow-600 px-6 py-3 font-semibold text-black transition hover:bg-yellow-500"
					>
						Fechar
					</button>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.slow-gif {
		animation-duration: 10s;
		animation-timing-function: steps(8, end);
		animation-iteration-count: infinite;
	}

	/* Container principal com tamanho fixo em relação à viewport */
	.fixed-container {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		overflow: auto;
	}

	/* Cardbox central com tamanho fixo */
	.game-card {
		min-height: 90vh;
		min-width: 90vw;
		max-height: 90vh;
		overflow-y: auto;
	}

	.bg {
		background-image: url('https://pbs.twimg.com/ext_tw_video_thumb/1537465478867722241/pu/img/JAQ7N8tFzPWNnQJ-.jpg');
		background-size: cover;
		background-position: center;
		background-attachment: fixed;
	}

	@keyframes shake {
		0%,
		100% {
			transform: translateX(0);
		}
		20%,
		60% {
			transform: translateX(-5px);
		}
		40%,
		80% {
			transform: translateX(5px);
		}
	}

	.shake {
		animation: shake 0.4s ease-in-out;
	}

	/* Nova animação para tremer a tela */
	@keyframes screen-shake {
		0%,
		100% {
			transform: translateX(0) translateY(0);
		}
		10%,
		30%,
		50%,
		70%,
		90% {
			transform: translateX(-10px) translateY(-5px);
		}
		20%,
		40%,
		60%,
		80% {
			transform: translateX(10px) translateY(5px);
		}
	}

	.animate-screen-shake {
		animation: screen-shake 0.3s ease-in-out;
	}

	@keyframes pulse {
		0%,
		100% {
			transform: scale(1);
			opacity: 1;
		}
		50% {
			transform: scale(1.02);
			opacity: 0.9;
		}
	}

	.animate-pulse {
		animation: pulse 0.5s ease-in-out;
	}

	.animate-hit {
		animation: hit 0.6s ease-in-out;
	}

	.font-orbitron {
		font-family: 'Orbitron', sans-serif;
	}

	/* Estilos para o dropdown de música */
	#musicDropdown {
		transition: all 0.3s ease;
	}

	/* Estilos responsivos */
	@media (max-width: 768px) {
		.relative.h-32.w-32 {
			width: 80px;
			height: 80px;
		}

		h1.font-orbitron {
			font-size: 2rem;
			margin-bottom: 1rem;
		}

		.grid.grid-cols-2.gap-4 {
			grid-template-columns: 1fr;
		}

		button.p-4.text-xl {
			padding: 0.75rem;
			font-size: 1rem;
		}

		/* Ajustes para o menu de música em mobile */
		#musicDropdown {
			width: 200px;
			right: -50px;
		}
	}
</style>
