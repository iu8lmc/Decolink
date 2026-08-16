#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""I testi della guida: francese, spagnolo, portoghese, olandese."""

G2 = {}

G2["fr"] = {
    "titolo": "Decodium Mobile via Decolink",
    "sottotitolo": "Comment amener l'audio de la radio — et la commande du poste — de "
                   "l'ordinateur de la station jusqu'au téléphone : à la maison sur le même "
                   "réseau, ou n'importe où en passant par le serveur.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · protocole HFGW v2",
    "meta_data": "16 août 2026",

    "h_prima": "Avant de commencer",
    "s1_t": "Sur l'ordinateur",
    "s1_p": "<strong>Decolink</strong> lancé à côté de la radio, avec le CODEC USB du poste "
            "branché. C'est lui qui envoie l'audio et, si vous voulez, sert le CAT.",
    "s2_t": "Sur le téléphone",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Tout se règle au même endroit : l'engrenage ⚙ "
            "en haut, sections <em>Station</em>, <em>Audio</em> et <em>CAT / Rig</em>.",
    "s3_t": "Uniquement pour le relais",
    "s3_p": "Un compte approuvé sur <code>decolink.ft2.it</code>. En réseau local il n'en faut "
            "pas : aucune inscription, rien ne sort de la maison.",

    "h_tre": "Les trois liaisons",
    "tre_p": "Decolink et Decodium Mobile doivent être sur le <strong>même mode</strong> : "
             "c'est l'erreur la plus courante, et elle ne donne pas de message clair.",
    "th_modo": "Mode", "th_quando": "Quand", "th_chi": "Qui appelle qui",
    "th_porta": "Port", "th_aprire": "À ouvrir",
    "lan": "LAN", "lan_q": "Téléphone et ordinateur sur le même WiFi",
    "lan_c": "L'ordinateur envoie l'audio vers l'IP du téléphone", "lan_a": "Rien",
    "relay": "Relais", "relay_q": "Hors de chez soi, données mobiles comprises",
    "relay_c": "Les deux sortent vers le serveur", "relay_a": "Rien",
    "casa": "Maison", "casa_q": "Hors de chez soi, sans passer par le serveur",
    "casa_c": "Le téléphone appelle votre adresse de maison", "casa_a": "UDP 5555 sur le routeur",
    "tre_fine": "Le <strong>relais</strong> est celui qui marche toujours : aucun des deux n'a "
                "besoin d'être joignable depuis l'extérieur, puisque ce sont eux qui vont vers "
                "le serveur. C'est aussi le seul qui demande un compte.",

    "h_pa": "Parcours A · réseau local",
    "pa1_sigla": "Sur l'ordinateur · Decolink",
    "pa1_h3": "Envoyez l'audio à l'adresse du téléphone",
    "pa1_1": '<span class="dove">Audio radio</span> → choisissez le CODEC USB de l\'émetteur-'
             'récepteur.',
    "pa1_1n": "C'est l'entrée par laquelle arrive le signal reçu, pas le micro de l'ordinateur.",
    "pa1_2": '<span class="dove">Mode</span> → <code>LAN direct</code>',
    "pa1_3": '<span class="dove">Hôte</span> → l\'adresse IP du téléphone sur le WiFi de la '
             'maison.',
    "pa1_3n": "Sur le téléphone vous la trouvez dans Réglages → WiFi → le réseau auquel vous "
              "êtes connecté. Elle ressemble à 192.168.1.42.",
    "pa1_4": '<span class="dove">Port</span> → <code>5555</code>',
    "pa1_5": 'Appuyez sur <span class="dove">Démarrer</span>. Le niveau doit bouger au rythme '
             'du bruit de bande.',
    "pa2_sigla": "Sur le téléphone · Decodium Mobile",
    "pa2_h3": "Mettez-vous à l'écoute",
    "pa2_1": '⚙ → <span class="dove">Station</span> : indicatif, locator, report.',
    "pa2_1n": "Sans indicatif ni locator les messages ne peuvent pas être composés.",
    "pa2_2": '<span class="dove">Audio → Liaison</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Port</span> → <code>5555</code>, le même que dans Decolink',
    "pa2_4": 'Appuyez sur <span class="dove">Recevoir</span>. <em>« À l\'écoute sur le port '
             '5555 »</em> apparaît : à partir de là le waterfall se remplit dès que '
             'l\'ordinateur commence à émettre.',
    "pa_avv_t": "En LAN le téléphone attend, il n'appelle pas",
    "pa_avv_p": "C'est l'ordinateur qui doit connaître l'IP du téléphone. Si le routeur "
                "distribue les adresses à tour de rôle, demain cette IP sera à quelqu'un "
                "d'autre et l'audio n'arrivera plus : réservez au téléphone une adresse fixe "
                "dans le routeur, ou revérifiez le champ <em>Hôte</em> à chaque séance.",

    "h_pb": "Parcours B · relais sur le serveur",
    "pb1_sigla": "Une seule fois · depuis le navigateur",
    "pb1_h3": "Demandez l'accès à la station",
    "pb1_1": "Ouvrez <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Renseignez e-mail, mot de passe, indicatif et la station à laquelle vous voulez "
             "vous connecter.",
    "pb1_3": "Attendez l'approbation.",
    "pb1_3n": "La demande reste en attente jusqu'à ce que le titulaire de la station l'accepte : "
              "c'est lui qui décide, ce n'est pas automatique. C'est lui aussi qui fixe votre "
              "rôle.",
    "ruolo_tit": "Titulaire",
    "ruolo_tit_d": 'écoute et émet <span class="libero">— c\'est sa station</span>',
    "ruolo_op": "Opérateur",
    "ruolo_op_d": 'écoute et émet <span class="libero">— autorisé par le titulaire</span>',
    "ruolo_asc": "Auditeur",
    "ruolo_asc_d": 'réception seule <span class="libero">— la touche d\'émission reste '
                   'éteinte</span>',
    "pb2_sigla": "Sur l'ordinateur · Decolink",
    "pb2_h3": "Faites entrer la station dans le relais",
    "pb2_1": '<span class="dove">Serveur</span> → <code>decolink.ft2.it</code>, puis e-mail et '
             'mot de passe, et appuyez sur <span class="dove">Se connecter</span>.',
    "pb2_1n": "Si vous laissez la station allumée toute seule, cochez « retenir le mot de "
              "passe » : au redémarrage elle repart sans personne au clavier.",
    "pb2_2": '<span class="dove">Mode</span> → <code>Relais + station</code>',
    "pb2_3": '<span class="dove">Hôte</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Port</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Profil</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "Les profils compressés consomment un cinquième de la bande, mais gardez-les pour "
              "plus tard : vérifiez d'abord que la liaison tient comme ça.",
    "pb2_5": 'Appuyez sur <span class="dove">Démarrer</span>.',
    "pb3_sigla": "Sur le téléphone · Decodium Mobile",
    "pb3_h3": "Connectez-vous avec vos identifiants",
    "pb3_1": '⚙ → <span class="dove">Audio → Liaison</span> → <code>Relais</code>',
    "pb3_2": 'Remplissez les champs de connexion et appuyez sur <span class="dove">Entrer</span>.',
    "pb3_3": "Regardez la ligne d'état : elle doit indiquer votre indicatif, la station et le "
             "rôle.",
    "pb3_3n": "Si vous lisez « Vous êtes entré comme auditeur », vous recevez mais n'émettez "
              "pas : c'est le rôle, pas une panne.",
    "pb3_4": '<span class="dove">Port</span> → <code>5555</code>, puis '
             '<span class="dove">Recevoir</span>.',
    "campi_acc": "Connexion",
    "campi_email": "E-mail", "campi_email_d": "celui avec lequel vous vous êtes inscrit",
    "campi_pw": "Mot de passe", "campi_pw_d": "celui du compte Decolink",
    "campi_relay": "Relais", "campi_relay_d": "laissez vide : il prend l'adresse de connexion",
    "campi_porta": "Port",
    "pb_avv_t": "L'autorisation dure une heure",
    "pb_avv_p": "Le serveur délivre un laissez-passer qui expire au bout de soixante minutes. "
                "Avec <em>« Retenir le mot de passe »</em> activé, l'application le renouvelle "
                "toute seule une minute avant ; sans, au bout d'une heure l'audio s'arrête sans "
                "explication et il faut se reconnecter à la main. Sur le téléphone le mot de "
                "passe reste dans le trousseau chiffré du système, hors des sauvegardes.",

    "h_pc": "Parcours C · le téléphone appelle la maison",
    "pc_p": "Pour qui ne veut pas passer par le serveur et dispose d'une adresse joignable de "
            "l'extérieur. En échange il faut mettre les mains dans le routeur.",
    "pc_1": '<span class="dove">Sur le routeur</span> : redirigez le port <code>UDP 5555</code> '
            'vers l\'adresse de l\'ordinateur de la station.',
    "pc_2": '<span class="dove">Dans Decolink</span> : mode <code>Le téléphone appelle la '
            'maison</code>, port <code>5555</code>. Le champ Hôte reste vide : c\'est le '
            'téléphone qui se manifeste.',
    "pc_3": '<span class="dove">Sur le téléphone</span> : liaison <code>Maison</code>, dans le '
            'champ adresse votre nom DynDNS (par exemple <code>iu8lmc.ddns.net</code>), port '
            '<code>5555</code>, puis <span class="dove">Recevoir</span>.',
    "pc_fine": "Avec une connexion domestique derrière un CG-NAT — beaucoup de fibres et "
               "presque toutes les lignes mobiles — ce mode ne peut pas fonctionner : personne "
               "de l'extérieur n'arrive à vous joindre. C'est exactement le cas pour lequel le "
               "relais existe.",

    "h_cat": "Commander la radio",
    "cat_p": "L'audio et le CAT sont deux choses distinctes : on peut recevoir sans CAT, mais "
             "sans CAT le téléphone ne sait pas sur quelle fréquence vous êtes et ne peut ni "
             "changer de bande ni passer en émission.",
    "cat_th1": "Source", "cat_th2": "Comment ça se connecte", "cat_th3": "Où ça marche",
    "cat_r1": "TCP vers le PC",
    "cat_r1d": 'Dans Decolink cochez <em>« Servir le CAT au téléphone »</em> ; sur le téléphone '
               'mettez l\'IP de l\'ordinateur et le port <span class="num">4532</span>',
    "cat_r1w": "Réseau local",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Un câble du téléphone à la radio, sans ordinateur entre les deux",
    "cat_r2w": "Partout, avec la radio à portée de câble",
    "cat_r3": "Canal audio",
    "cat_r3d": "Les commandes voyagent dans la liaison audio déjà ouverte",
    "cat_r3w": "Partout — c'est le bon choix avec Relais ou Maison",
    "cat_fine": "Avec le <em>canal audio</em> il n'y a rien de plus à ouvrir : pour que ça "
                "marche, deux conditions — l'audio réseau déjà démarré, et le CAT allumé dans "
                "Decolink.",

    "h_guai": "Quand rien n'arrive",
    "g1_m": "« À l'écoute sur le port 5555 — le PC doit envoyer l'audio ici »",
    "g1_c": "Vous êtes en mode <strong>LAN</strong> alors que vous vouliez le relais. En LAN le "
            "téléphone se contente d'attendre : aucun enregistrement ne part, et vous attendez "
            "un audio que personne n'enverra. Passez la liaison en <em>Relais</em>.",
    "g2_m": "« Nom non résolu »",
    "g2_c": "L'adresse saisie n'existe pas, ou le téléphone n'a pas de réseau. Vérifiez que "
            "vous n'avez pas mis <code>https://</code> dans le champ du relais.",
    "g3_m": "« Port 5555 occupé »",
    "g3_c": "Une autre application tient ce port. Fermez-la, ou prenez-en un autre — en le "
            "changeant dans les deux programmes.",
    "g4_m": "« serveur injoignable »",
    "g4_c": "C'est un problème de liaison, pas de mot de passe : l'application distingue les "
            "deux exprès. Vérifiez que vous avez du réseau et réessayez.",
    "g5_m": "L'audio démarre et s'arrête après quelques secondes",
    "g5_c": "Le relais écarte ceux qui restent muets quinze secondes. Si cela se répète, le "
            "réseau perd des paquets : essayez un profil compressé, qui occupe un cinquième de "
            "la bande.",
    "g6_m": "Le waterfall bouge mais rien ne se décode",
    "g6_c": "Presque toujours c'est l'horloge : les modes numériques tiennent ou tombent à la "
            "seconde près. Laissez le téléphone prendre l'heure sur le réseau.",

    "h_demo": "Essayer sans radio",
    "demo_p": "La touche <strong>Démo</strong>, à côté de <em>Recevoir</em>, allume une bande "
              "factice avec cinq stations et des décodages qui défilent. Elle sert à voir "
              "comment se comporte l'application avant de brancher quoi que ce soit — utile "
              "pour apprendre où regarder, avant d'aller chercher une panne qui n'existe pas.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — les valeurs indiquées sont celles par "
             "défaut des deux programmes au 16 août 2026.",
}

G2["es"] = {
    "titolo": "Decodium Mobile sobre Decolink",
    "sottotitolo": "Cómo llevar el audio de la radio — y el mando del equipo — del ordenador de "
                   "la estación al teléfono: en casa sobre la misma red, o en cualquier sitio "
                   "pasando por el servidor.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · protocolo HFGW v2",
    "meta_data": "16 de agosto de 2026",

    "h_prima": "Antes de empezar",
    "s1_t": "En el ordenador",
    "s1_p": "<strong>Decolink</strong> en marcha junto a la radio, con el CODEC USB del equipo "
            "conectado. Es él quien manda el audio y, si quieres, sirve el CAT.",
    "s2_t": "En el teléfono",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Todo se configura en un solo sitio: el "
            "engranaje ⚙ de arriba, secciones <em>Estación</em>, <em>Audio</em> y "
            "<em>CAT / Rig</em>.",
    "s3_t": "Solo para el relé",
    "s3_p": "Una cuenta aprobada en <code>decolink.ft2.it</code>. En red local no hace falta: "
            "ni registro, ni datos fuera de casa.",

    "h_tre": "Las tres conexiones",
    "tre_p": "Decolink y Decodium Mobile tienen que estar en el <strong>mismo modo</strong>: es "
             "el fallo más común, y no da mensajes claros.",
    "th_modo": "Modo", "th_quando": "Cuándo", "th_chi": "Quién llama a quién",
    "th_porta": "Puerto", "th_aprire": "Que abrir",
    "lan": "LAN", "lan_q": "Teléfono y ordenador en el mismo WiFi",
    "lan_c": "El ordenador dispara el audio a la IP del teléfono", "lan_a": "Nada",
    "relay": "Relé", "relay_q": "Fuera de casa, también con datos móviles",
    "relay_c": "Los dos salen hacia el servidor", "relay_a": "Nada",
    "casa": "Casa", "casa_q": "Fuera de casa, sin pasar por el servidor",
    "casa_c": "El teléfono llama a tu dirección de casa", "casa_a": "UDP 5555 en el router",
    "tre_fine": "El <strong>relé</strong> es el que funciona siempre: ninguno de los dos tiene "
                "que ser accesible desde fuera, porque son ellos los que se asoman al servidor. "
                "Es también el único que pide una cuenta.",

    "h_pa": "Camino A · red local",
    "pa1_sigla": "En el ordenador · Decolink",
    "pa1_h3": "Manda el audio a la dirección del teléfono",
    "pa1_1": '<span class="dove">Audio radio</span> → elige el CODEC USB del transceptor.',
    "pa1_1n": "Es la entrada por la que llega la señal recibida, no el micrófono del ordenador.",
    "pa1_2": '<span class="dove">Modalidad</span> → <code>LAN directa</code>',
    "pa1_3": '<span class="dove">Host</span> → la dirección IP del teléfono en el WiFi de casa.',
    "pa1_3n": "En el teléfono la ves en Ajustes → WiFi → la red a la que estás conectado. Se "
              "parece a 192.168.1.42.",
    "pa1_4": '<span class="dove">Puerto</span> → <code>5555</code>',
    "pa1_5": 'Pulsa <span class="dove">Iniciar</span>. El nivel tiene que moverse al ritmo del '
             'ruido de banda.',
    "pa2_sigla": "En el teléfono · Decodium Mobile",
    "pa2_h3": "Ponte a la escucha",
    "pa2_1": '⚙ → <span class="dove">Estación</span>: indicativo, locator, informe.',
    "pa2_1n": "Sin indicativo y locator los mensajes no se pueden componer.",
    "pa2_2": '<span class="dove">Audio → Conexión</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Puerto</span> → <code>5555</code>, el mismo puesto en Decolink',
    "pa2_4": 'Pulsa <span class="dove">Recibir</span>. Aparece <em>«Escuchando en el puerto '
             '5555»</em>: desde ese momento el waterfall se llena en cuanto el ordenador '
             'empieza a mandar.',
    "pa_avv_t": "En LAN el teléfono espera, no llama",
    "pa_avv_p": "Es el ordenador el que tiene que conocer la IP del teléfono. Si el router "
                "reparte las direcciones por turnos, mañana esa IP será de otro y el audio ya "
                "no llegará: reserva al teléfono una dirección fija en el router, o vuelve a "
                "comprobar el campo <em>Host</em> en cada sesión.",

    "h_pb": "Camino B · relé en el servidor",
    "pb1_sigla": "Una sola vez · desde el navegador",
    "pb1_h3": "Pide el acceso a la estación",
    "pb1_1": "Abre <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Rellena correo, contraseña, indicativo y la estación a la que quieres conectarte.",
    "pb1_3": "Espera la aprobación.",
    "pb1_3n": "La solicitud queda pendiente hasta que el titular de la estación la acepta: "
              "decide él, no es automático. Es él quien fija también tu papel.",
    "ruolo_tit": "Titular",
    "ruolo_tit_d": 'escucha y transmite <span class="libero">— la estación es suya</span>',
    "ruolo_op": "Operador",
    "ruolo_op_d": 'escucha y transmite <span class="libero">— autorizado por el titular</span>',
    "ruolo_asc": "Oyente",
    "ruolo_asc_d": 'solo recepción <span class="libero">— la tecla de transmisión sigue '
                   'apagada</span>',
    "pb2_sigla": "En el ordenador · Decolink",
    "pb2_h3": "Mete la estación dentro del relé",
    "pb2_1": '<span class="dove">Servidor</span> → <code>decolink.ft2.it</code>, luego correo y '
             'contraseña, y pulsa <span class="dove">Acceder</span>.',
    "pb2_1n": "Si dejas la estación encendida sola, marca «recordar la contraseña»: al "
              "reiniciar arranca sin nadie al teclado.",
    "pb2_2": '<span class="dove">Modalidad</span> → <code>Relé + estación</code>',
    "pb2_3": '<span class="dove">Host</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Puerto</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Perfil</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "Los perfiles comprimidos consumen un quinto del ancho de banda, pero déjalos "
              "para después: primero comprueba que el enlace aguanta así.",
    "pb2_5": 'Pulsa <span class="dove">Iniciar</span>.',
    "pb3_sigla": "En el teléfono · Decodium Mobile",
    "pb3_h3": "Entra con tus credenciales",
    "pb3_1": '⚙ → <span class="dove">Audio → Conexión</span> → <code>Relé</code>',
    "pb3_2": 'Rellena los campos del acceso y pulsa <span class="dove">Entrar</span>.',
    "pb3_3": "Mira la línea de estado: tiene que decir tu indicativo, la estación y el papel.",
    "pb3_3n": "Si lees «Has entrado como oyente», recibes pero no transmites: es el papel, no "
              "una avería.",
    "pb3_4": '<span class="dove">Puerto</span> → <code>5555</code>, luego '
             '<span class="dove">Recibir</span>.',
    "campi_acc": "Acceso",
    "campi_email": "Correo", "campi_email_d": "el que usaste al registrarte",
    "campi_pw": "Contraseña", "campi_pw_d": "la de la cuenta de Decolink",
    "campi_relay": "Relé", "campi_relay_d": "déjalo vacío: coge la dirección del acceso",
    "campi_porta": "Puerto",
    "pb_avv_t": "El permiso dura una hora",
    "pb_avv_p": "El servidor entrega un salvoconducto que caduca a los sesenta minutos. Con "
                "<em>«Recordar la contraseña»</em> activado la aplicación lo renueva sola un "
                "minuto antes; sin él, al cabo de una hora el audio se para sin explicaciones y "
                "hay que volver a entrar a mano. En el teléfono la contraseña vive en el "
                "llavero cifrado del sistema, fuera de las copias de seguridad.",

    "h_pc": "Camino C · el teléfono llama a casa",
    "pc_p": "Sirve a quien no quiere pasar por el servidor y tiene una dirección accesible desde "
            "fuera. A cambio hay que meter las manos en el router.",
    "pc_1": '<span class="dove">En el router</span>: redirige el puerto <code>UDP 5555</code> '
            'hacia la dirección del ordenador de la estación.',
    "pc_2": '<span class="dove">En Decolink</span>: modalidad <code>El teléfono llama a '
            'casa</code>, puerto <code>5555</code>. El campo Host queda vacío: es el teléfono '
            'el que se asoma.',
    "pc_3": '<span class="dove">En el teléfono</span>: conexión <code>Casa</code>, en el campo '
            'de la dirección tu nombre DynDNS (por ejemplo <code>iu8lmc.ddns.net</code>), '
            'puerto <code>5555</code>, luego <span class="dove">Recibir</span>.',
    "pc_fine": "Con una conexión de casa detrás de CG-NAT — muchas fibras y casi todas las "
               "líneas móviles — este modo no puede funcionar: nadie desde fuera consigue "
               "alcanzarte. Es exactamente el caso para el que existe el relé.",

    "h_cat": "Mandar la radio",
    "cat_p": "El audio y el CAT son dos cosas separadas: puedes recibir sin CAT, pero sin CAT el "
             "teléfono no sabe en qué frecuencia estás y no puede cambiar de banda ni pasar a "
             "transmisión.",
    "cat_th1": "Fuente", "cat_th2": "Cómo se conecta", "cat_th3": "Dónde funciona",
    "cat_r1": "TCP al PC",
    "cat_r1d": 'En Decolink marca <em>«Sirve el CAT al teléfono»</em>; en el teléfono pon la IP '
               'del ordenador y el puerto <span class="num">4532</span>',
    "cat_r1w": "Red local",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Cable del teléfono a la radio, sin ordenador de por medio",
    "cat_r2w": "En cualquier sitio, con la radio al alcance del cable",
    "cat_r3": "Canal de audio",
    "cat_r3d": "Los mandos viajan dentro del enlace de audio ya abierto",
    "cat_r3w": "En cualquier sitio — es la elección correcta con Relé o Casa",
    "cat_fine": "Con el <em>canal de audio</em> no hay que abrir nada más: para que funcione "
                "tienen que darse dos condiciones — el audio de red ya iniciado, y el CAT "
                "encendido en Decolink.",

    "h_guai": "Cuando no llega nada",
    "g1_m": "«Escuchando en el puerto 5555 — el PC tiene que mandar aquí el audio»",
    "g1_c": "Estás en modo <strong>LAN</strong> pero querías el relé. En LAN el teléfono solo "
            "espera: no sale ningún registro, y te quedas esperando un audio que nadie mandará. "
            "Cambia la conexión a <em>Relé</em>.",
    "g2_m": "«Nombre no resuelto»",
    "g2_c": "La dirección escrita no existe, o el teléfono está sin red. Comprueba que no has "
            "incluido <code>https://</code> en el campo del relé.",
    "g3_m": "«Puerto 5555 ocupado»",
    "g3_c": "Otra aplicación tiene ese puerto. Ciérrala, o usa otro — cambiándolo en los dos "
            "programas.",
    "g4_m": "«servidor inaccesible»",
    "g4_c": "Es un problema de conexión, no de contraseña: la aplicación distingue los dos "
            "casos a propósito. Comprueba que tienes red y vuelve a intentarlo.",
    "g5_m": "El audio arranca y se para a los pocos segundos",
    "g5_c": "El relé descarta a quien se queda callado quince segundos. Si pasa continuamente, "
            "la red está perdiendo paquetes: prueba un perfil comprimido, que ocupa un quinto "
            "del ancho de banda.",
    "g6_m": "El waterfall se mueve pero no decodifica nada",
    "g6_c": "Casi siempre es el reloj: los modos digitales se sostienen o caen en el segundo "
            "exacto. Deja que el teléfono coja la hora de la red.",

    "h_demo": "Probar sin radio",
    "demo_p": "El botón <strong>Demo</strong>, junto a <em>Recibir</em>, enciende una banda "
              "fingida con cinco estaciones y decodificaciones que van pasando. Sirve para ver "
              "cómo se comporta la aplicación antes de conectar nada — útil para aprender dónde "
              "mirar, antes de ir a buscar una avería que no existe.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — los valores indicados son los "
             "predeterminados de los dos programas a 16 de agosto de 2026.",
}

G2["pt"] = {
    "titolo": "Decodium Mobile através do Decolink",
    "sottotitolo": "Como levar o áudio do rádio — e o comando do equipamento — do computador da "
                   "estação até ao telemóvel: em casa na mesma rede, ou em qualquer lado "
                   "passando pelo servidor.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · protocolo HFGW v2",
    "meta_data": "16 de agosto de 2026",

    "h_prima": "Antes de começar",
    "s1_t": "No computador",
    "s1_p": "<strong>Decolink</strong> a correr ao lado do rádio, com o CODEC USB do "
            "equipamento ligado. É ele que envia o áudio e, se quiser, serve o CAT.",
    "s2_t": "No telemóvel",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Tudo se configura num só sítio: a engrenagem ⚙ "
            "em cima, secções <em>Estação</em>, <em>Áudio</em> e <em>CAT / Rig</em>.",
    "s3_t": "Só para o relé",
    "s3_p": "Uma conta aprovada em <code>decolink.ft2.it</code>. Em rede local não é precisa: "
            "sem registo, nada sai de casa.",

    "h_tre": "As três ligações",
    "tre_p": "O Decolink e o Decodium Mobile têm de estar no <strong>mesmo modo</strong>: é o "
             "erro mais comum, e não dá mensagens claras.",
    "th_modo": "Modo", "th_quando": "Quando", "th_chi": "Quem chama quem",
    "th_porta": "Porta", "th_aprire": "A abrir",
    "lan": "LAN", "lan_q": "Telemóvel e computador no mesmo WiFi",
    "lan_c": "O computador dispara o áudio para o IP do telemóvel", "lan_a": "Nada",
    "relay": "Relé", "relay_q": "Fora de casa, também com dados móveis",
    "relay_c": "Os dois saem para o servidor", "relay_a": "Nada",
    "casa": "Casa", "casa_q": "Fora de casa, sem passar pelo servidor",
    "casa_c": "O telemóvel liga para o seu endereço de casa", "casa_a": "UDP 5555 no router",
    "tre_fine": "O <strong>relé</strong> é o que funciona sempre: nenhum dos dois precisa de ser "
                "alcançável do exterior, porque são ambos a procurar o servidor. É também o "
                "único que exige uma conta.",

    "h_pa": "Percurso A · rede local",
    "pa1_sigla": "No computador · Decolink",
    "pa1_h3": "Envie o áudio para o endereço do telemóvel",
    "pa1_1": '<span class="dove">Áudio do rádio</span> → escolha o CODEC USB do transcetor.',
    "pa1_1n": "É a entrada por onde chega o sinal recebido, não o microfone do computador.",
    "pa1_2": '<span class="dove">Modalidade</span> → <code>LAN direta</code>',
    "pa1_3": '<span class="dove">Servidor</span> → o endereço IP do telemóvel no WiFi de casa.',
    "pa1_3n": "No telemóvel encontra-o em Definições → WiFi → a rede a que está ligado. Parece-se "
              "com 192.168.1.42.",
    "pa1_4": '<span class="dove">Porta</span> → <code>5555</code>',
    "pa1_5": 'Carregue em <span class="dove">Iniciar</span>. O nível deve mexer-se ao ritmo do '
             'ruído de banda.',
    "pa2_sigla": "No telemóvel · Decodium Mobile",
    "pa2_h3": "Ponha-se à escuta",
    "pa2_1": '⚙ → <span class="dove">Estação</span>: indicativo, locator, relatório.',
    "pa2_1n": "Sem indicativo e locator as mensagens não se conseguem compor.",
    "pa2_2": '<span class="dove">Áudio → Ligação</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Porta</span> → <code>5555</code>, a mesma escrita no Decolink',
    "pa2_4": 'Carregue em <span class="dove">Receber</span>. Aparece <em>«À escuta na porta '
             '5555»</em>: a partir daí o waterfall enche-se assim que o computador começa a '
             'enviar.',
    "pa_avv_t": "Em LAN o telemóvel espera, não liga",
    "pa_avv_p": "É o computador que tem de saber o IP do telemóvel. Se o router distribui os "
                "endereços à vez, amanhã esse IP será de outro e o áudio deixa de chegar: "
                "reserve ao telemóvel um endereço fixo no router, ou volte a verificar o campo "
                "<em>Servidor</em> em cada sessão.",

    "h_pb": "Percurso B · relé no servidor",
    "pb1_sigla": "Uma só vez · pelo navegador",
    "pb1_h3": "Peça o acesso à estação",
    "pb1_1": "Abra <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Preencha email, palavra-passe, indicativo e a estação a que se quer ligar.",
    "pb1_3": "Aguarde a aprovação.",
    "pb1_3n": "O pedido fica à espera até o titular da estação o aceitar: decide ele, não é "
              "automático. É ele que define também o seu papel.",
    "ruolo_tit": "Titular",
    "ruolo_tit_d": 'escuta e transmite <span class="libero">— a estação é dele</span>',
    "ruolo_op": "Operador",
    "ruolo_op_d": 'escuta e transmite <span class="libero">— autorizado pelo titular</span>',
    "ruolo_asc": "Ouvinte",
    "ruolo_asc_d": 'apenas receção <span class="libero">— a tecla de transmissão fica '
                   'apagada</span>',
    "pb2_sigla": "No computador · Decolink",
    "pb2_h3": "Leve a estação para dentro do relé",
    "pb2_1": '<span class="dove">Servidor</span> → <code>decolink.ft2.it</code>, depois email e '
             'palavra-passe, e carregue em <span class="dove">Entrar</span>.',
    "pb2_1n": "Se deixar a estação ligada sozinha, marque «lembrar a palavra-passe»: ao "
              "reiniciar arranca sem ninguém ao teclado.",
    "pb2_2": '<span class="dove">Modalidade</span> → <code>Relé + estação</code>',
    "pb2_3": '<span class="dove">Servidor</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Porta</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Perfil</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "Os perfis comprimidos gastam um quinto da largura de banda, mas guarde-os para "
              "depois: verifique primeiro que a ligação aguenta assim.",
    "pb2_5": 'Carregue em <span class="dove">Iniciar</span>.',
    "pb3_sigla": "No telemóvel · Decodium Mobile",
    "pb3_h3": "Entre com as suas credenciais",
    "pb3_1": '⚙ → <span class="dove">Áudio → Ligação</span> → <code>Relé</code>',
    "pb3_2": 'Preencha os campos do acesso e carregue em <span class="dove">Entrar</span>.',
    "pb3_3": "Veja a linha de estado: deve dizer o seu indicativo, a estação e o papel.",
    "pb3_3n": "Se ler «Entrou como ouvinte», recebe mas não transmite: é o papel, não uma avaria.",
    "pb3_4": '<span class="dove">Porta</span> → <code>5555</code>, depois '
             '<span class="dove">Receber</span>.',
    "campi_acc": "Acesso",
    "campi_email": "Email", "campi_email_d": "aquele com que se registou",
    "campi_pw": "Palavra-passe", "campi_pw_d": "a da conta Decolink",
    "campi_relay": "Relé", "campi_relay_d": "deixe vazio: usa o endereço do acesso",
    "campi_porta": "Porta",
    "pb_avv_t": "A autorização dura uma hora",
    "pb_avv_p": "O servidor emite um salvo-conduto que expira ao fim de sessenta minutos. Com "
                "<em>«Lembrar a palavra-passe»</em> ativo a aplicação renova-o sozinha um "
                "minuto antes; sem isso, ao fim de uma hora o áudio para sem explicações e tem "
                "de voltar a entrar à mão. No telemóvel a palavra-passe fica no porta-chaves "
                "cifrado do sistema, fora das cópias de segurança.",

    "h_pc": "Percurso C · o telemóvel liga para casa",
    "pc_p": "Serve a quem não quer passar pelo servidor e tem um endereço alcançável do "
            "exterior. Em troca é preciso meter as mãos no router.",
    "pc_1": '<span class="dove">No router</span>: encaminhe a porta <code>UDP 5555</code> para o '
            'endereço do computador da estação.',
    "pc_2": '<span class="dove">No Decolink</span>: modalidade <code>O telemóvel liga para '
            'casa</code>, porta <code>5555</code>. O campo Servidor fica vazio: é o telemóvel '
            'que se dá a conhecer.',
    "pc_3": '<span class="dove">No telemóvel</span>: ligação <code>Casa</code>, no campo do '
            'endereço o seu nome DynDNS (por exemplo <code>iu8lmc.ddns.net</code>), porta '
            '<code>5555</code>, depois <span class="dove">Receber</span>.',
    "pc_fine": "Com uma ligação doméstica atrás de CG-NAT — muitas fibras e quase todas as "
               "linhas móveis — este modo não pode funcionar: ninguém de fora consegue "
               "alcançá-lo. É exatamente o caso para o qual o relé existe.",

    "h_cat": "Comandar o rádio",
    "cat_p": "O áudio e o CAT são duas coisas separadas: pode receber sem CAT, mas sem CAT o "
             "telemóvel não sabe em que frequência está e não pode mudar de banda nem pôr em "
             "transmissão.",
    "cat_th1": "Origem", "cat_th2": "Como se liga", "cat_th3": "Onde funciona",
    "cat_r1": "TCP para o PC",
    "cat_r1d": 'No Decolink marque <em>«Servir o CAT ao telemóvel»</em>; no telemóvel ponha o IP '
               'do computador e a porta <span class="num">4532</span>',
    "cat_r1w": "Rede local",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Cabo do telemóvel ao rádio, sem computador pelo meio",
    "cat_r2w": "Em qualquer lado, com o rádio ao alcance do cabo",
    "cat_r3": "Canal de áudio",
    "cat_r3d": "Os comandos viajam dentro da ligação de áudio já aberta",
    "cat_r3w": "Em qualquer lado — é a escolha certa com Relé ou Casa",
    "cat_fine": "Com o <em>canal de áudio</em> não é preciso abrir mais nada: para funcionar "
                "têm de ser verdade duas coisas — o áudio de rede já iniciado, e o CAT ligado "
                "no Decolink.",

    "h_guai": "Quando não chega nada",
    "g1_m": "«À escuta na porta 5555 — o PC tem de enviar o áudio para aqui»",
    "g1_c": "Está em modo <strong>LAN</strong> mas queria o relé. Em LAN o telemóvel só espera: "
            "não sai nenhum registo, e fica à espera de um áudio que ninguém vai enviar. Mude a "
            "ligação para <em>Relé</em>.",
    "g2_m": "«Nome não resolvido»",
    "g2_c": "O endereço escrito não existe, ou o telemóvel está sem rede. Verifique que não "
            "incluiu <code>https://</code> no campo do relé.",
    "g3_m": "«Porta 5555 ocupada»",
    "g3_c": "Outra aplicação está a segurar essa porta. Feche-a, ou use outra — mudando-a nos "
            "dois programas.",
    "g4_m": "«servidor inacessível»",
    "g4_c": "É um problema de ligação, não de palavra-passe: a aplicação distingue os dois casos "
            "de propósito. Verifique que tem rede e tente de novo.",
    "g5_m": "O áudio arranca e para ao fim de poucos segundos",
    "g5_c": "O relé descarta quem fica calado quinze segundos. Se acontece a toda a hora, a "
            "rede está a perder pacotes: experimente um perfil comprimido, que ocupa um quinto "
            "da largura de banda.",
    "g6_m": "O waterfall mexe-se mas não descodifica nada",
    "g6_c": "Quase sempre é o relógio: os modos digitais vivem ou morrem no segundo exato. Deixe "
            "o telemóvel ir buscar a hora à rede.",

    "h_demo": "Experimentar sem rádio",
    "demo_p": "O botão <strong>Demo</strong>, ao lado de <em>Receber</em>, acende uma banda "
              "fingida com cinco estações e descodificações a passar. Serve para ver como se "
              "porta a aplicação antes de ligar seja o que for — útil para perceber onde olhar, "
              "antes de ir procurar uma avaria que não existe.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — os valores indicados são os predefinidos "
             "dos dois programas a 16 de agosto de 2026.",
}

G2["nl"] = {
    "titolo": "Decodium Mobile via Decolink",
    "sottotitolo": "Hoe je de audio van de set — en de bediening ervan — van de shackcomputer "
                   "naar je telefoon brengt: thuis op hetzelfde netwerk, of overal via de "
                   "server.",
    "meta_app": "Decodium 4.0 Mobile",
    "meta_proto": "Decolink · protocol HFGW v2",
    "meta_data": "16 augustus 2026",

    "h_prima": "Voor je begint",
    "s1_t": "Op de computer",
    "s1_p": "<strong>Decolink</strong> draait naast de set, met de USB-CODEC van de set "
            "aangesloten. Die stuurt de audio en levert desgewenst de CAT.",
    "s2_t": "Op de telefoon",
    "s2_p": "<strong>Decodium 4 Mobile</strong>. Alles wordt op één plek ingesteld: het "
            "tandwiel ⚙ bovenaan, secties <em>Station</em>, <em>Audio</em> en "
            "<em>CAT / Rig</em>.",
    "s3_t": "Alleen voor de relay",
    "s3_p": "Een goedgekeurd account op <code>decolink.ft2.it</code>. Op een lokaal netwerk is "
            "dat niet nodig: geen registratie, niets verlaat het huis.",

    "h_tre": "De drie verbindingen",
    "tre_p": "Decolink en Decodium Mobile moeten in dezelfde <strong>modus</strong> staan: dat "
             "is de meest gemaakte fout, en hij geeft geen duidelijke melding.",
    "th_modo": "Modus", "th_quando": "Wanneer", "th_chi": "Wie belt wie",
    "th_porta": "Poort", "th_aprire": "Openzetten",
    "lan": "LAN", "lan_q": "Telefoon en computer op dezelfde WiFi",
    "lan_c": "De computer schiet de audio naar het IP van de telefoon", "lan_a": "Niets",
    "relay": "Relay", "relay_q": "Buitenshuis, ook op mobiele data",
    "relay_c": "Allebei gaan ze naar de server", "relay_a": "Niets",
    "casa": "Thuis", "casa_q": "Buitenshuis, zonder de server",
    "casa_c": "De telefoon belt jouw thuisadres", "casa_a": "UDP 5555 op de router",
    "tre_fine": "De <strong>relay</strong> is degene die altijd werkt: geen van beide hoeft van "
                "buitenaf bereikbaar te zijn, want ze melden zich allebei zelf bij de server. "
                "Het is ook de enige die een account vereist.",

    "h_pa": "Route A · lokaal netwerk",
    "pa1_sigla": "Op de computer · Decolink",
    "pa1_h3": "Stuur de audio naar het adres van de telefoon",
    "pa1_1": '<span class="dove">Audio van de set</span> → kies de USB-CODEC van de zendontvanger.',
    "pa1_1n": "Dat is de ingang waarop het ontvangen signaal binnenkomt, niet de microfoon van "
              "de computer.",
    "pa1_2": '<span class="dove">Modus</span> → <code>Direct LAN</code>',
    "pa1_3": '<span class="dove">Host</span> → het IP-adres van de telefoon op de WiFi thuis.',
    "pa1_3n": "Op de telefoon vind je het in Instellingen → WiFi → het netwerk waarmee je "
              "verbonden bent. Het lijkt op 192.168.1.42.",
    "pa1_4": '<span class="dove">Poort</span> → <code>5555</code>',
    "pa1_5": 'Druk op <span class="dove">Starten</span>. Het niveau moet meebewegen met de '
             'bandruis.',
    "pa2_sigla": "Op de telefoon · Decodium Mobile",
    "pa2_h3": "Ga luisteren",
    "pa2_1": '⚙ → <span class="dove">Station</span>: roepnaam, locator, rapport.',
    "pa2_1n": "Zonder roepnaam en locator kunnen de berichten niet worden samengesteld.",
    "pa2_2": '<span class="dove">Audio → Verbinding</span> → <code>LAN</code>',
    "pa2_3": '<span class="dove">Poort</span> → <code>5555</code>, dezelfde als in Decolink',
    "pa2_4": 'Druk op <span class="dove">Ontvangen</span>. Er verschijnt <em>“Luistert op poort '
             '5555”</em>: vanaf dat moment loopt de waterfall vol zodra de computer begint te '
             'zenden.',
    "pa_avv_t": "Op LAN wacht de telefoon, hij belt niet",
    "pa_avv_p": "Het is de computer die het IP van de telefoon moet kennen. Deelt de router de "
                "adressen bij toerbeurt uit, dan is dat IP morgen van iemand anders en komt de "
                "audio niet meer aan: reserveer in de router een vast adres voor de telefoon, "
                "of controleer het veld <em>Host</em> elke sessie opnieuw.",

    "h_pb": "Route B · relay op de server",
    "pb1_sigla": "Eenmalig · vanuit de browser",
    "pb1_h3": "Vraag toegang tot het station",
    "pb1_1": "Open <code>https://decolink.ft2.it/registrati</code>",
    "pb1_2": "Vul e-mail, wachtwoord, roepnaam in en het station waarmee je wilt verbinden.",
    "pb1_3": "Wacht op goedkeuring.",
    "pb1_3n": "Het verzoek blijft open tot de stationseigenaar het accepteert: hij beslist, het "
              "gaat niet vanzelf. Hij bepaalt ook jouw rol.",
    "ruolo_tit": "Eigenaar",
    "ruolo_tit_d": 'luistert en zendt <span class="libero">— het is zijn station</span>',
    "ruolo_op": "Operator",
    "ruolo_op_d": 'luistert en zendt <span class="libero">— gemachtigd door de eigenaar</span>',
    "ruolo_asc": "Luisteraar",
    "ruolo_asc_d": 'alleen ontvangen <span class="libero">— de zendtoets blijft uit</span>',
    "pb2_sigla": "Op de computer · Decolink",
    "pb2_h3": "Breng het station de relay binnen",
    "pb2_1": '<span class="dove">Server</span> → <code>decolink.ft2.it</code>, dan e-mail en '
             'wachtwoord, en druk op <span class="dove">Aanmelden</span>.',
    "pb2_1n": "Laat je het station alleen draaien, vink dan “wachtwoord onthouden” aan: na een "
              "herstart komt het terug zonder dat er iemand achter het toetsenbord zit.",
    "pb2_2": '<span class="dove">Modus</span> → <code>Relay + station</code>',
    "pb2_3": '<span class="dove">Host</span> → <code>decolink.ft2.it</code> · '
             '<span class="dove">Poort</span> → <code>5555</code>',
    "pb2_4": '<span class="dove">Profiel</span> → <code>PCM 48 kHz</code>',
    "pb2_4n": "De gecomprimeerde profielen gebruiken een vijfde van de bandbreedte, maar bewaar "
              "ze voor later: kijk eerst of de verbinding het zo houdt.",
    "pb2_5": 'Druk op <span class="dove">Starten</span>.',
    "pb3_sigla": "Op de telefoon · Decodium Mobile",
    "pb3_h3": "Meld je aan met je gegevens",
    "pb3_1": '⚙ → <span class="dove">Audio → Verbinding</span> → <code>Relay</code>',
    "pb3_2": 'Vul de aanmeldvelden in en druk op <span class="dove">Inloggen</span>.',
    "pb3_3": "Kijk naar de statusregel: daar moeten je roepnaam, het station en de rol staan.",
    "pb3_3n": "Staat er “Je bent binnen als luisteraar”, dan ontvang je wel maar zend je niet: "
              "dat is de rol, geen storing.",
    "pb3_4": '<span class="dove">Poort</span> → <code>5555</code>, dan '
             '<span class="dove">Ontvangen</span>.',
    "campi_acc": "Aanmelden",
    "campi_email": "E-mail", "campi_email_d": "die waarmee je je hebt geregistreerd",
    "campi_pw": "Wachtwoord", "campi_pw_d": "dat van je Decolink-account",
    "campi_relay": "Relay", "campi_relay_d": "leeg laten: hij neemt het aanmeldadres",
    "campi_porta": "Poort",
    "pb_avv_t": "De toestemming duurt een uur",
    "pb_avv_p": "De server geeft een pasje af dat na zestig minuten verloopt. Met "
                "<em>“Wachtwoord onthouden”</em> aan vernieuwt de app het een minuut van "
                "tevoren vanzelf; zonder stopt de audio na een uur zonder uitleg en moet je met "
                "de hand opnieuw inloggen. Op de telefoon staat het wachtwoord in de versleutelde "
                "sleutelbos van het systeem, buiten de back-ups.",

    "h_pc": "Route C · de telefoon belt naar huis",
    "pc_p": "Voor wie liever niet via de server gaat en een van buitenaf bereikbaar adres heeft. "
            "In ruil daarvoor moet je in de router duiken.",
    "pc_1": '<span class="dove">Op de router</span>: stuur poort <code>UDP 5555</code> door naar '
            'het adres van de shackcomputer.',
    "pc_2": '<span class="dove">In Decolink</span>: modus <code>De telefoon belt naar huis</code>, '
            'poort <code>5555</code>. Het veld Host blijft leeg: de telefoon meldt zich.',
    "pc_3": '<span class="dove">Op de telefoon</span>: verbinding <code>Thuis</code>, in het '
            'adresveld je DynDNS-naam (bijvoorbeeld <code>iu8lmc.ddns.net</code>), poort '
            '<code>5555</code>, dan <span class="dove">Ontvangen</span>.',
    "pc_fine": "Met een thuisaansluiting achter CG-NAT — veel glasvezel en vrijwel elke mobiele "
               "lijn — kan deze modus niet werken: niemand van buiten bereikt je. Precies "
               "daarvoor bestaat de relay.",

    "h_cat": "De set bedienen",
    "cat_p": "Audio en CAT zijn twee losse dingen: ontvangen kan zonder CAT, maar zonder CAT "
             "weet de telefoon niet op welke frequentie je zit en kan hij niet van band "
             "wisselen of laten zenden.",
    "cat_th1": "Bron", "cat_th2": "Hoe het verbindt", "cat_th3": "Waar het werkt",
    "cat_r1": "TCP naar de pc",
    "cat_r1d": 'Vink in Decolink <em>“Lever de CAT aan de telefoon”</em> aan; zet op de telefoon '
               'het IP van de computer en poort <span class="num">4532</span>',
    "cat_r1w": "Lokaal netwerk",
    "cat_r2": "USB-OTG",
    "cat_r2d": "Een kabel van telefoon naar set, geen computer ertussen",
    "cat_r2w": "Overal, met de set binnen kabelbereik",
    "cat_r3": "Audiokanaal",
    "cat_r3d": "De commando's lopen mee in de al open audioverbinding",
    "cat_r3w": "Overal — de juiste keuze bij Relay of Thuis",
    "cat_fine": "Bij het <em>audiokanaal</em> hoeft er niets extra open: er moeten twee dingen "
                "kloppen — de netwerkaudio is al gestart, en CAT staat aan in Decolink.",

    "h_guai": "Als er niets binnenkomt",
    "g1_m": "“Luistert op poort 5555 — de pc moet de audio hierheen sturen”",
    "g1_c": "Je staat in <strong>LAN</strong>-modus maar je wilde de relay. Op LAN wacht de "
            "telefoon alleen maar: er gaat geen registratie uit, en je zit te wachten op audio "
            "die niemand stuurt. Zet de verbinding op <em>Relay</em>.",
    "g2_m": "“Naam niet herleid”",
    "g2_c": "Het ingevulde adres bestaat niet, of de telefoon heeft geen netwerk. Controleer of "
            "je geen <code>https://</code> in het relayveld hebt gezet.",
    "g3_m": "“Poort 5555 bezet”",
    "g3_c": "Een andere app houdt die poort vast. Sluit hem, of neem een andere — en wijzig hem "
            "in allebei de programma's.",
    "g4_m": "“server onbereikbaar”",
    "g4_c": "Dit is een verbindingsprobleem, geen wachtwoordprobleem: de app houdt die twee "
            "expres uit elkaar. Kijk of je netwerk hebt en probeer opnieuw.",
    "g5_m": "De audio start en stopt na een paar seconden",
    "g5_c": "De relay gooit eruit wie vijftien seconden stil blijft. Gebeurt het steeds, dan "
            "verliest het netwerk pakketten: probeer een gecomprimeerd profiel, dat een vijfde "
            "van de bandbreedte gebruikt.",
    "g6_m": "De waterfall beweegt maar er wordt niets gedecodeerd",
    "g6_c": "Bijna altijd is het de klok: digitale modes staan of vallen op de exacte seconde. "
            "Laat de telefoon de tijd van het netwerk halen.",

    "h_demo": "Uitproberen zonder set",
    "demo_p": "De knop <strong>Demo</strong>, naast <em>Ontvangen</em>, zet een verzonnen band "
              "aan met vijf stations en voorbijrollende decodes. Hij laat zien hoe de app zich "
              "gedraagt voordat er iets is aangesloten — handig om te leren waar je moet "
              "kijken, voordat je op zoek gaat naar een storing die er niet is.",

    "piede": "Decodium 4 Mobile · Decolink · IU8LMC — de genoemde waarden zijn de "
             "standaardinstellingen van beide programma's op 16 augustus 2026.",
}
