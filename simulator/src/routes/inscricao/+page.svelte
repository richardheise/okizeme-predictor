<script>
	import { onMount } from 'svelte';

	let experiencia = '';
	let nivelLuta = '3';
	let nivelEstocastico = '3';

	// Verifica se já há dados salvos no localStorage
	onMount(() => {
		const dadosSalvos = localStorage.getItem('dadosUsuario');
		if (dadosSalvos) {
			window.location.href = '/okizeme';
		}
	});

	// Função para salvar dados, com validação
	function salvarDados() {
		if (!experiencia) {
			alert('Por favor, responda a pergunta sobre jogos de luta antes de prosseguir.');
			return; // Impede que o usuário avance
		}

		const dadosUsuario = {
			experiencia,
			nivelLuta: parseInt(nivelLuta),
			nivelEstocastico: parseInt(nivelEstocastico),
			jogadas: [] // campo reservado para uso posterior
		};

		localStorage.setItem('dadosUsuario', JSON.stringify(dadosUsuario));
		window.location.href = '/okizeme'; // Redireciona após salvar
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
			class="h-[70%] w-full max-w-3xl overflow-auto rounded-2xl border-4 border-blue-600 bg-[rgba(0,0,0,0.8)] p-8 shadow-2xl backdrop-blur-md"
		>
			<h2
				class="mb-6 text-3xl font-bold text-cyan-300"
				style="font-family: 'Orbitron', sans-serif;"
			>
				Antes de começarmos, precisamos de algumas informações!
			</h2>

			<!-- Subtexto -->
			<p class="text-sm text-gray-300">Não se preocupe, isso não muda a dificuldade do jogo ;)</p>

			<form class="space-y-6 text-left text-white">
				<div>
					<label class="mb-2 block font-semibold">Você já jogou jogos de luta antes?</label>
					<select
						bind:value={experiencia}
						class="bg-opacity-70 w-full rounded-lg border border-gray-500 bg-black p-3 text-white focus:ring-2 focus:ring-cyan-500 focus:outline-none"
					>
						<option value="">Selecione...</option>
						<option value="sim">Sim</option>
						<option value="não">Não</option>
					</select>
				</div>

				<div>
					<label class="mb-2 block font-semibold">
						Qual seu nível de conhecimento em jogos de luta? (1 a 5)
					</label>
					<div class="flex justify-between">
						<span>Nunca joguei</span>
						<span>Já ouvi falar</span>
						<span>Joguei</span>
						<span>Jogo bastante</span>
						<span>Jogo todo dia</span>
					</div>
					<input type="range" min="1" max="5" bind:value={nivelLuta} class="w-full" />
				</div>

				<div>
					<label class="mb-2 block font-semibold">
						Qual seu nível de conhecimento sobre modelos estocásticos? (1 a 5)
					</label>
					<div class="flex justify-between">
						<span>Não conheço</span>
						<span>Já ouvi falar</span>
						<span>Conheço</span>
						<span>Conheço bem</span>
						<span>Conheço muito bem</span>
					</div>
					<input type="range" min="1" max="5" bind:value={nivelEstocastico} class="w-full" />
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
