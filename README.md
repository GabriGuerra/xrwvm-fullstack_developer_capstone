To do
- [ ] Testar a rota /fetchDealers com outros estados além de Kansas
Verificar se a API responde corretamente com diferentes estados para garantir que o filtro funciona como esperado.
- [ ] Verificar se o front-end está consumindo corretamente a API
Garantir que o React (ou outro cliente) está fazendo as requisições para a rota correta e recebendo os dados do backend.
- [ ] Validar integração com o serviço de análise de sentimentos
Testar se os textos enviados estão sendo analisados corretamente e os resultados estão sendo tratados no app.
- [ ] Documentar endpoints e exemplos de uso da API
Criar documentação com exemplos de requisições e respostas da API para facilitar testes e integração com o front.
- [ ] Criar script para popular o MongoDB com mais dados de dealers
Facilitar testes automatizados com um seed de dados mais variado.

In progress
- [ ] Revisar a estrutura do Dockerfile para incluir apenas os arquivos necessários
Evitar empacotar arquivos desnecessários e garantir que a imagem final seja leve e eficiente.
- [ ] Refatorar a API para adicionar tratamento de erro mais detalhado
Adicionar mensagens claras para status como 404 (nenhum dealer encontrado), 500 (erro interno), etc.

Done
- [x] Inserir logs de requisição no app.js
Adicionar console.log() para rastrear requisições recebidas e parâmetros usados.
- [x] Confirmar que o Express não estava rodando o código atualizado
Verificado via testes e ausência de logs após requisições.
- [x] Atualizar docker-compose.yml com a seção de build e contexto correto
Adicionado build.context e dockerfile para forçar o uso do código atualizado da IDE.
- [x] Reconstruir containers com --no-cache
Build forçado sem cache antigo para garantir atualização de código no container.
- [x] Validar rota com curl e navegador
Testado com múltiplas abordagens para confirmar que a rota responde conforme esperado.
- [x] Confirmar funcionamento dos logs e rota /fetchDealers/Kansas
Logs de requisição, estado e resultado visíveis no terminal.
- [x] Verificar que os recursos da IBM Cloud não foram afetados
Confirmação de que o analisador de sentimentos e arquivos externos continuam disponíveis.
