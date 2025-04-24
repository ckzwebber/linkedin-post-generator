# LinkedIn Post Generator

Script em Python que gera automaticamente posts diários sobre tecnologias como React.js, Node.js, TypeScript, entre outras, e envia por e-mail. Utiliza um modelo LLM local via API e traduz os textos para português.

## Funcionalidades

- Geração diária de conteúdo com base em uma lista de tecnologias
- Tradução automática do post para português
- Envio do conteúdo por e-mail de forma automatizada
- Log de execução com erros e status de envio

## Tecnologias utilizadas

- Python
- dotenv
- requests
- smtplib (e-mail)
- LLM local via API (Ollama)

## Variáveis de ambiente

Crie um arquivo `.env` com os seguintes campos:

```env
SENDER_EMAIL=seu@email.com
RECEIVER_EMAIL=destinatario@email.com
EMAIL_PASSWORD=sua_senha
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
OLLAMA_API_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3
```

## Execução

Para rodar o script manualmente:

```bash
python linkedin_post_generator.py
```

## Observações

- Certifique-se de que a API local esteja ativa (`OLLAMA_API_URL`)
- O envio de e-mails requer configuração válida de SMTP
- Os posts são gerados com base na data do dia e a posição da tecnologia na lista

## Logs

Os logs são salvos em `linkedin-post-generator.log` para facilitar o rastreio de erros e execuções.

---

## 👤 Autor

Desenvolvido por [Carlos Miguel Webber Miguel](https://www.linkedin.com/in/cmiguelwm/)  
Entre em contato para dúvidas, sugestões ou colaborações!

---

## 📄 Licença

Este projeto está licenciado sob a licença [MIT](LICENSE).
