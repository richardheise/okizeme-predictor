<script>
	function continuar() {
		window.location.href = '/inscricao';
	}
</script>

<div class="relative h-screen w-screen overflow-hidden text-white">
	<!-- Fundo com imagem -->
	<div class="absolute inset-0 -z-10 flex">
		<div
			class="h-full w-full bg-cover bg-center"
			style="
				background-image: url('https://images.steamusercontent.com/ugc/769481826559933621/2F8718A8738D8F18C17B2D0CB7CAF1DF40389A5D/?imw=5000&imh=5000&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false');
			"
		></div>
	</div>

	<!-- Conteúdo centralizado -->
	<div class="flex h-full flex-col items-center justify-center px-4 text-center">
		<div
			class="h-[75%] w-full overflow-auto rounded-2xl border-4 border-blue-600 bg-[rgba(0,0,0,0.9)] p-8 shadow-2xl backdrop-blur-md"
		>
			<h2
				class="mb-6 text-4xl font-bold text-cyan-300"
				style="font-family: 'Orbitron', sans-serif;"
			>
				Ações
			</h2>

			<!-- Texto de explicação -->
			<p class="mb-4 text-lg text-white">
				Suas possíveis ações na <span class="font-semibold text-red-500">ofensiva</span> são as seguintes:
			</p>

			<ul class="mb-6 text-lg font-medium text-red-400">
				<li>Agarrão</li>
				<li>Combo com Atraso</li>
				<li>Meaty Alto</li>
				<li>Meaty Baixo</li>
				<li>Shimmy com Parry Baixo</li>
			</ul>

			<p class="mb-4 text-lg text-white">
				Suas possíveis ações na <span class="font-semibold text-blue-400">defensiva</span> são as seguintes:
			</p>

			<ul class="text-lg font-medium text-blue-300">
				<li>Defender</li>
				<li>Guard-jump</li>
				<li>Botão</li>
				<li>Agarrão</li>
				<li>Reversal</li>
				<li>Parry Alto</li>
				<li>Parry Baixo</li>
			</ul>

			<!-- Botão Continuar -->
			<div class="mt-8 flex justify-center">
				<button
					on:click={continuar}
					class="mt-6 cursor-pointer rounded-xl border-2 border-blue-300 bg-blue-400 px-8 py-3 text-xl font-bold text-black shadow-lg transition hover:scale-105 hover:bg-blue-600 active:scale-95"
					style="font-family: 'Orbitron', sans-serif;"
				>
					Entendi!
				</button>
			</div>
		</div>
	</div>
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
</style>
