## Título

feat(comissoes/manutencao): melhorias de acessibilidade e layout responsivo

## Descrição
- Abas: ARIA (`aria-selected`, `aria-controls`), foco visível, badges com contraste.
- Formulário: `aria-label` nos tipos e preview com `aria-live`; `aria-labelledby` no form; botões com `aria-label`.
- Tabelas: `caption` oculto, `scope` nos cabeçalhos, `aria-label` nos botões.
- Base: link “Pular para o conteúdo”, `aria-expanded` no toggle da sidebar.
- CI: workflow de deploy para Railway via GitHub Actions.

## Impacto Visual/UX
- Layout responsivo mantido (Bootstrap). Foco visível melhora navegação por teclado.
- Nenhuma alteração disruptiva de estilos.

## Checklist
- [ ] Testado `/configuracoes/comissoes` com três abas.
- [ ] Healthcheck `/ping` respondendo `pong`.
- [ ] Executado localmente com `ALLOW_SQLITE_DEV=1`.
- [ ] Secrets `RAILWAY_TOKEN` e `RAILWAY_PROJECT_ID` configurados no GitHub.

## Pós-Deploy
- Validar `/login` e fluxo de vincular faixa Manutenção aos Técnicos.
- Monitorar `railway logs` para confirmar inicialização.
