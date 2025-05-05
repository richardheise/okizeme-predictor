<script>
	function continuar() {
		window.location.href = '/como-jogar';
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
				Regras
			</h2>

			<!-- Texto de explicação -->
			<p class="mb-4 text-lg font-semibold text-white">
				Em qualquer jogo de luta, se um jogador acertar um golpe específico no oponente, este pode
				ser derrubado. Durante esse estado de derrubada, o jogador que atacou ganha uma vantagem
				significativa e pode ditar a próxima ação — uma situação conhecida como okizeme (uma junção
				de termos japoneses que significa "ataque ao levantar"). Ao longo de uma partida, cada
				decisão do jogador é moldada pela tentativa de prever o próximo movimento do oponente; isso
				é especialmente verdadeiro em situações de okizeme, nas quais tanto o atacante quanto o
				defensor precisam recorrer a estratégias de adivinhação.
			</p>

			<p class="text-lg font-semibold text-gray-300">
				Neste simulador, você assumirá o papel de um jogador de Ken em uma partida espelhada.
				Buscando adivinhar corretamente as ações do seu oponente tanto na defesa quanto no ataque.
			</p>

			<br />

			<p class="text-lg font-semibold text-gray-300">
				Será um conjunto de partidas FT10 (Quem Vencer 10). Cada partida é composta por uma melhor
				de 2 rounds. Ou seja, se prepare para jogar bastante! Você terá uma barra de vida de 8
				pontos, assim como seu oponente. Caso vença a interação de okizeme, será seu turno de
				atacar! Caso perca, será a vez do seu oponente. Caso empate, ambos jogadores terão 50% de
				chance de voltar à ofensiva!
			</p>
			<br />

			<p class="text-lg text-gray-300">
				Se precisar de uma explicação visual, recomendamos o shorts abaixo:
			</p>

			<!-- Vídeo -->
			<div class="flex w-full items-center justify-center py-6">
				<iframe
					width="360"
					height="640"
					src="https://www.youtube.com/embed/sj1vmZZjOl4"
					title="YouTube video player"
					frameborder="0"
					allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
					allowfullscreen
				></iframe>
			</div>

			<!-- Botão Continuar -->
			<div class="mt-8 flex justify-center">
				<button
					on:click={continuar}
					class="mt-6 cursor-pointer rounded-xl border-2 border-red-300 bg-red-400 px-8 py-3 text-xl font-bold text-black shadow-lg transition hover:scale-105 hover:bg-red-600 active:scale-95"
					style="font-family: 'Orbitron', sans-serif;"
				>
					Continuar
				</button>
			</div>
		</div>
	</div>
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
</style>
