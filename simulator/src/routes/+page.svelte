<script>
	function irParaInscricao() {
		window.location.href = '/regras';
	}
</script>

<!-- Container principal com posição relativa -->
<div class="relative h-screen w-screen overflow-hidden text-white">
	<!-- Camada de fundo com imagem e opacidade (escondida no mobile) -->
	<div
		class="absolute inset-0 -z-10 hidden bg-cover bg-center opacity-90 md:block"
		style="background-image: url('https://cdn2.steamgriddb.com/grid/e681e2c709233b64149827928ba76df4.png');"
	></div>

	<!-- Conteúdo centralizado -->
	<div class="flex h-full flex-col items-center justify-center px-4 text-center">
		<div
			class="bg-opacity-90 h-full w-full overflow-auto border-0 bg-black p-6 text-white shadow-none md:h-[60%] md:w-[90%] md:max-w-5xl md:rounded-2xl md:border-4 md:border-red-600 md:bg-[rgba(0,0,0,0.8)] md:p-10 md:shadow-2xl md:backdrop-blur-md"
		>
			<h1
				class="mb-10 text-3xl font-bold text-yellow-300 md:mb-12 md:text-5xl"
				style="font-family: 'Orbitron', sans-serif;"
			>
				Bem-vindo ao futuro!<br />Sua luta começa aqui.
			</h1>

			<p class="text-base leading-relaxed font-semibold text-gray-200 md:text-xl">
				Este é um <span class="text-red-400">Simulador de Okizeme</span>, onde você enfrentará nossa
				inteligência artificial em combates intensos.<br /><br />
				Cada jogador possui <span class="text-yellow-300">8 pontos de vida</span>. O vencedor será
				aquele que conquistar <span class="text-green-400">10 partidas</span> primeiro.<br /><br />
				Uma partida é decidida em <span class="text-orange-400">melhor de 3 rounds</span>: quem
				vencer 2 rounds, leva a vitória da partida.<br /><br />
				Está pronto para desafiar o futuro e mostrar seu domínio nos momentos mais críticos do combate?
			</p>

			<!-- Botão Começar -->
			<button
				on:click={irParaInscricao}
				class="mt-6 cursor-pointer rounded-xl border-2 border-yellow-300 bg-yellow-400 px-8 py-3 text-xl font-bold text-black shadow-lg transition hover:scale-105 hover:bg-yellow-300 active:scale-95"
				style="font-family: 'Orbitron', sans-serif;"
			>
				Começar!
			</button>
		</div>
	</div>
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
</style>
