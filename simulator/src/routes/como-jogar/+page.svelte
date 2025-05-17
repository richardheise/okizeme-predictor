<script>
	import Tabela from '$lib/components/tabela.svelte';
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
	<div class="flex h-full flex-col items-center justify-center px-4">
		<div
			class="h-[85%] w-full overflow-auto rounded-2xl border-4 border-blue-600 bg-[rgba(0,0,0,0.9)] p-8 shadow-2xl backdrop-blur-md"
		>
			<!-- Título "Regras" no topo -->
			<h1 class="font-orbitron mb-6 text-center text-4xl font-bold text-white">COMO JOGAR</h1>

			<!-- Seção "Como Funciona" centralizada -->
			<div class="mb-8 rounded-lg bg-[rgba(20,20,20,0.7)] p-6 text-center">
				<h2 class="font-orbitron mb-4 text-2xl font-bold text-white">FUNCIONAMENTO</h2>
				<div class="mx-auto max-w-3xl space-y-4 text-lg font-semibold">
					<p>
						Nesta simulação, você participará de interações de combate inspiradas em jogos de luta,
						semelhantes a uma partida de "Pedra, Papel e Tesoura", mas com mais opções e
						profundidade tática.
					</p>
					<p>
						Cada ação <span class="font-semibold text-red-400">ofensiva</span> representa uma
						tentativa de pressionar ou abrir a defesa do oponente, enquanto cada ação
						<span class="font-semibold text-blue-400">defensiva</span> tem o objetivo de resistir ou
						reverter a ofensiva.
					</p>
					<p>
						As opções defensivas como "Reversal" ou "Botão" também causam dano se forem
						bem-sucedidas, mas são arriscadas — uma leitura errada pode resultar em grandes
						punições.
					</p>
				</div>
			</div>

			<!-- Ações Ofensivas e Defensivas lado a lado -->
			<div class="mb-8 grid grid-cols-1 gap-6 md:grid-cols-2">
				<!-- Ações Ofensivas -->
				<div class="rounded-lg bg-[rgba(30,0,0,0.6)] p-6">
					<h2 class="font-orbitron mb-4 text-center text-2xl font-bold text-red-400">
						AÇÕES OFENSIVAS
					</h2>
					<ul class="space-y-3 text-center text-lg font-medium text-red-300">
						<li class="rounded bg-[rgba(255,0,0,0.1)] p-2">
							1. Agarrão — Vence Defender, Botão e Parry (1 de dano)
						</li>
						<li class="rounded bg-[rgba(255,0,0,0.1)] p-2">
							2. Combo com Atraso — Vence Guard-Jump(3.5), Parry Baixo(3.5) e Reversal(3)
						</li>
						<li class="rounded bg-[rgba(255,0,0,0.1)] p-2">
							3. Meaty Alto — Vence Agarrão, Parry Baixo, botão, com 3.5 de dano
						</li>
						<li class="rounded bg-[rgba(255,0,0,0.1)] p-2">
							4. Meaty Baixo — Vence Agarrão, Parry alto e botão, com 2.5 de dano
						</li>
						<li class="rounded bg-[rgba(255,0,0,0.1)] p-2">
							5. Shimmy — Vence Agarrão(3) e Reversal(3.5)
						</li>
					</ul>
				</div>

				<!-- Ações Defensivas -->
				<div class="rounded-lg bg-[rgba(0,0,30,0.6)] p-6">
					<h2 class="font-orbitron mb-4 text-center text-2xl font-bold text-blue-400">
						AÇÕES DEFENSIVAS
					</h2>
					<ul class="space-y-3 text-center text-lg font-semibold text-blue-300">
						<li class="rounded bg-[rgba(0,0,255,0.1)] p-2">
							1. Defender — Vence Combo c/ Atraso, Meaty e Shimmy
						</li>
						<li class="rounded bg-[rgba(0,0,255,0.1)] p-2">
							2. Guard-jump — Vence Agarrão, Meaty e Shimmy
						</li>
						<li class="rounded bg-[rgba(0,0,255,0.1)] p-2">
							3. Botão — Vence Shimmy(3), Combo com Atraso(3.5)
						</li>
						<li class="rounded bg-[rgba(0,0,255,0.1)] p-2">
							4. Agarrão — Vence Combo c/ Atraso(1)
						</li>
						<li class="rounded bg-[rgba(0,0,255,0.1)] p-2">
							5. Reversal — Vence Agarrão e Meaty, com 1.4 de dano
						</li>
						<li class="rounded bg-[rgba(0,0,255,0.1)] p-2">
							6. Parry Alto — Vence Combo c/ Atraso e Meaty Alto, com 3.5 de dano
						</li>
						<li class="rounded bg-[rgba(0,0,255,0.1)] p-2">
							7. Parry Baixo — Vence Meaty baixo (3.5)
						</li>
					</ul>
				</div>
			</div>

			<!-- Seção da Tabela -->
			<div class="mb-6 rounded-lg bg-[rgba(20,20,20,0.7)] p-4">
				<h3 class="font-orbitron mb-4 text-center text-3xl font-bold text-white">
					TABELA DE INTERAÇÕES
				</h3>

				<!-- Instruções sobre como ler a tabela -->
				<div class="mb-6 text-center text-lg font-semibold">
					<p class="mt-4 text-center">
						A tabela abaixo detalha todas as interações possíveis entre ações ofensivas e
						defensivas.
						<span class="font-semibold text-yellow-400"
							><br />
							Como ler:</span
						> as linhas representam suas ações ofensivas e as colunas as defensivas, os valores estão
						aplicado do ponto de vista do agressor, ou seja, a primeira linha pode ser lida como: agarrão
						vence defender e causa 1 de dano; perde para guard-jump sem levar dano; vence botão e causa
						1 de dano; perde para agarrão defensivo e não recebe dano; perde para reversals recebendo
						1.4 de dano e vence os parries causando 1 de dano.
					</p>
					<br />
					<p class="mb-4 text-center">
						Cada combinação mostra quem leva dano e em que quantidade.
						<span class="text-yellow-400"
							>Esta tabela estará disponível durante toda a partida para consulta. E lembre-se:
							jogos de luta são melhores com música ;)</span
						>
					</p>
				</div>

				<div class="overflow-x-auto">
					<div class="flex min-w-[600px] justify-center">
						<Tabela />
					</div>
				</div>
			</div>

			<!-- Botão Entendi -->
			<div class="mt-6 flex justify-center">
				<button
					on:click={continuar}
					class="font-orbitron cursor-pointer rounded-xl border-2 border-blue-300 bg-blue-400 px-8 py-3 text-xl font-bold text-black shadow-lg transition hover:scale-105 hover:bg-blue-600 active:scale-95"
				>
					ENTENDI!
				</button>
			</div>
		</div>
	</div>
</div>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
	.font-orbitron {
		font-family: 'Orbitron', sans-serif;
	}
</style>
