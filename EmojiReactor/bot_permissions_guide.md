# Guide de Configuration des Permissions Discord

## Étapes pour configurer correctement votre bot Discord :

### 1. Permissions du Bot dans le Portail Développeur

Allez sur https://discord.com/developers/applications et sélectionnez votre application :

**Dans l'onglet "Bot" :**
- Activez "MESSAGE CONTENT INTENT" (obligatoire)
- Activez "SERVER MEMBERS INTENT" 
- Activez "GUILD MESSAGES" sous Privileged Gateway Intents

### 2. Permissions OAuth2 pour l'Invitation

**Dans l'onglet "OAuth2" > "URL Generator" :**

Cochez ces scopes :
- `bot`
- `applications.commands`

Cochez ces permissions bot :
- `View Channels`
- `Send Messages` 
- `Read Message History`
- `Add Reactions`
- `Attach Files`

### 3. Inviter le Bot sur votre Serveur

1. Copiez l'URL générée en bas de la page OAuth2
2. Ouvrez cette URL dans votre navigateur
3. Sélectionnez votre serveur Discord
4. Confirmez les permissions

### 4. Permissions sur le Canal Discord

Dans votre serveur Discord :
1. Clic droit sur le canal concerné > "Modifier le canal"
2. Onglet "Permissions"
3. Ajoutez votre bot avec ces permissions :
   - Voir les messages
   - Envoyer des messages
   - Lire l'historique des messages
   - Ajouter des réactions

## URL d'Invitation Recommandée

Remplacez YOUR_CLIENT_ID par l'ID de votre application :

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=274877975552&scope=bot%20applications.commands
```

Cette URL contient toutes les permissions nécessaires pour le bot de reconnaissance d'images.