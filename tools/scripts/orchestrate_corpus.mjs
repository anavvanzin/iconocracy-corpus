import { OpenMultiAgent } from '@jackchen_me/open-multi-agent';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '../..');

// 1. Configurar os perfis dos Agentes
const scoutAgent = {
  name: 'scout',
  model: 'claude-sonnet-4-6',
  systemPrompt: `Você é um arquivista acadêmico especializado em imagens jurídicas do século XIX-XX.
  Sua tarefa é analisar as lacunas do corpus e planejar queries específicas de busca na Gallica para capturar imagens de Arquitetura Forense (Marianne/Justitia em prédios públicos, tribunais, etc.).`,
  tools: ['bash', 'file_read'],
};

const analystAgent = {
  name: 'analyst',
  model: 'claude-sonnet-4-6',
  systemPrompt: `Você é o IconoCode. Sua função é analisar as imagens fornecidas, aplicar a metodologia Panofsky de 3 níveis,
  e codificar os 10 indicadores ordinais de purificação clássica (desincorporacao, rigidez_postural, dessexualizacao, etc.) de 0 a 3.`,
  tools: ['bash', 'file_write', 'file_read'],
};

const reviewerAgent = {
  name: 'reviewer',
  model: 'claude-sonnet-4-6',
  systemPrompt: `Você é o Validador. Você deve garantir que as novas fichas geradas atendam às regras do schema oficial
  e não criem registros duplicados ou malformados.`,
  tools: ['bash', 'grep', 'file_read', 'file_edit'],
};

// 2. Inicializar o Orquestrador Multi-Agente
const orchestrator = new OpenMultiAgent({
  defaultModel: 'claude-sonnet-4-6',
  onProgress: (event) => console.log(`[EVENT] ${event.type}: ${event.task ?? event.agent ?? ''}`),
});

const team = orchestrator.createTeam('corpus-enrichment-team', {
  name: 'corpus-enrichment-team',
  agents: [scoutAgent, analystAgent, reviewerAgent],
  sharedMemory: true,
});

// 3. Executar o Pipeline de Enriquecimento
async function run() {
  console.log('Iniciando pipeline de enriquecimento do corpus...');
  const result = await orchestrator.runTasks(team, [
    {
      title: 'Mapear Lacunas e Buscar',
      description: `Analise as lacunas no arquivo ${path.join(REPO_ROOT, 'data/processed/records.jsonl')} e planeje buscas direcionadas.`,
      assignee: 'scout',
    },
    {
      title: 'Análise Visual e Codificação',
      description: 'Execute as inferências visuais locais para preencher os dados dos suportes e atributos ordinais.',
      assignee: 'analyst',
      dependsOn: ['Mapear Lacunas e Buscar'],
    },
    {
      title: 'Validação e Integração',
      description: `Rode o validador 'python ${path.join(REPO_ROOT, 'tools/scripts/validate_schemas.py')}' e integre as novas fichas de forma idempotente.`,
      assignee: 'reviewer',
      dependsOn: ['Análise Visual e Codificação'],
    }
  ]);

  console.log(`Pipeline concluído com sucesso: ${result.success}`);
}

run().catch(console.error);
