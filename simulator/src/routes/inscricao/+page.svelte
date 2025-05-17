<script>
	import { onMount } from 'svelte';
	const API_URL = 'https://okizeme.c3sl.ufpr.br/api';

	let nivelLuta = '';
	let nivelEstocastico = '';

	// Verifica se já há dados salvos no sessionStorage
	onMount(() => {
		const dadosSalvos = sessionStorage.getItem('dadosUsuario');
		if (dadosSalvos) {
			window.location.href = '/okizeme';
		}
	});

	// Função para salvar dados, com validação
	async function salvarDados() {
		if (!nivelLuta) {
			alert('Por favor, selecione seu nível de conhecimento em jogos de luta.');
			return;
		}
		if (!nivelEstocastico) {
			alert('Por favor, selecione seu nível de conhecimento sobre modelos estocásticos.');
			return;
		}

		const dadosUsuario = {
			nivelLuta: parseInt(nivelLuta),
			nivelEstocastico: parseInt(nivelEstocastico)
		};

		sessionStorage.setItem('dadosUsuario', JSON.stringify(dadosUsuario));

		try {
			// Enviar nível do jogador para o backend
			await fetch(`${API_URL}/enrollment`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ data: dadosUsuario })
			});
		} catch (e) {
			console.error('Erro ao enviar inscrição.');
		}

		window.location.href = '/okizeme';
	}
</script>

<div class="relative h-screen w-screen overflow-hidden text-white">
	<!-- Fundo com imagem -->
	<div
		class="absolute inset-0 -z-10 bg-cover bg-center opacity-80"
		style="background-image: url('https://images3.alphacoders.com/218/218637.jpg');"
	></div>

	<!-- Conteúdo centralizado -->
	<div class="flex h-full flex-col items-center justify-center px-4 text-center">
		<div
			class="h-[70%] w-[80%] overflow-auto rounded-2xl border-4 border-blue-600 bg-[rgba(0,0,0,0.8)] p-8 shadow-2xl backdrop-blur-md"
		>
			<h2
				class="mb-6 text-3xl font-bold text-cyan-300"
				style="font-family: 'Orbitron', sans-serif;"
			>
				Antes de começarmos, precisamos de algumas informações!
			</h2>

			<p class="text-sm text-gray-300">Todos os campos são obrigatórios</p>
			<br />
			<br />

			<form class="space-y-6 text-left text-white">
				<div>
					<label for="Jogos" class="mb-2 block text-center text-xl font-semibold">
						Qual seu nível de conhecimento em jogos de luta?*
					</label>
					<select
						bind:value={nivelLuta}
						class="bg-opacity-70 w-full rounded-lg border border-gray-500 bg-black p-3 text-white focus:ring-2 focus:ring-cyan-500 focus:outline-none"
						required
					>
						<option value="">Selecione...</option>
						<option value="1">1 - Nunca joguei</option>
						<option value="2">2 - Já ouvi falar</option>
						<option value="3">3 - Joguei</option>
						<option value="4">4 - Jogo bastante</option>
						<option value="5">5 - Jogo todo dia</option>
					</select>
				</div>
				<br />

				<div>
					<label for="Conhecimento" class="mb-2 block text-center text-xl font-semibold">
						Qual seu nível de conhecimento sobre modelos estocásticos?*
					</label>
					<select
						bind:value={nivelEstocastico}
						class="bg-opacity-70 w-full rounded-lg border border-gray-500 bg-black p-3 text-white focus:ring-2 focus:ring-cyan-500 focus:outline-none"
						required
					>
						<option value="">Selecione...</option>
						<option value="1">1 - Não conheço</option>
						<option value="2">2 - Já ouvi falar</option>
						<option value="3">3 - Conheço</option>
						<option value="4">4 - Conheço bem</option>
						<option value="5">5 - Conheço muito bem</option>
					</select>
				</div>

				<button
					type="button"
					on:click={salvarDados}
					class="mt-4 w-full cursor-pointer rounded-xl border-2 border-cyan-400 bg-cyan-300 px-8 py-3 text-xl font-bold text-black shadow-lg transition hover:scale-105 hover:bg-cyan-200 active:scale-95"
					style="font-family: 'Orbitron', sans-serif;"
				>
					Salvar e continuar
				</button>
			</form>
		</div>
	</div>
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
</style>
