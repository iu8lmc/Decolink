#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La guida «Decodium Mobile su Decolink», costruita dai testi tradotti.

La pagina originale era un file HTML scritto in italiano, con il testo mescolato
alla struttura. Qui struttura e testo sono separati: lo scheletro sta in questa
funzione, le parole in guida_testi*.py, una voce per lingua.

Cosi' una correzione alla pagina vale per tutte e sedici le lingue, e una
correzione a una traduzione non rischia di rompere il markup.

Nei testi restano i tag che fanno parte della frase — <strong>, <em>, <code> —
perche' cadono in punti diversi a seconda della lingua e spezzarli in tre pezzi
renderebbe le traduzioni illeggibili a chi le scrive.
"""


def costruisci(t: dict, e) -> str:
    """L'HTML della guida nella lingua data. `e` e' la funzione di escape.

    Le chiavi che finiscono in `_n` sono le note sotto un passo; quelle che
    contengono markup voluto da noi non passano da e(), le altre si'.
    """

    def passo(testo: str, nota: str = "") -> str:
        n = f'<span class="nota">{nota}</span>' if nota else ""
        return f"<li><span>{testo}{n}</span></li>"

    def scheda(titolo: str, corpo: str) -> str:
        return f'<div class="scheda"><h4>{e(titolo)}</h4><p>{corpo}</p></div>'

    def sintomo(msg: str, cura: str) -> str:
        return (f'<div class="sintomo"><span class="msg">{e(msg)}</span>'
                f'<span class="cura">{cura}</span></div>')

    # La scala di sintonia in testa alla pagina: e' un disegno, non un'immagine
    # da scaricare, cosi' non c'e' una richiesta in piu' e non manca mai.
    tacche = ""
    for i, x in enumerate(range(0, 801, 80)):
        alta = 4 if x % 400 == 0 else (10 if (x // 80) % 2 == 0 else 14)
        tacche += f'<line x1="{x}" y1="{alta}" x2="{x}" y2="25" />'
    scala = (f'<svg class="scala" viewBox="0 0 800 26" preserveAspectRatio="none" '
             f'role="presentation" aria-hidden="true">'
             f'<g stroke="currentColor" stroke-width="1" opacity=".35">'
             f'<line x1="0" y1="25" x2="800" y2="25" />{tacche}</g></svg>')

    return f"""
<div class="guida">
  <header class="g-testata">
    {scala}
    <h1>{e(t["titolo"])}</h1>
    <p class="g-sub">{e(t["sottotitolo"])}</p>
    <div class="g-meta">
      <span>{e(t["meta_app"])}</span>
      <span>{e(t["meta_proto"])}</span>
      <span>{e(t["meta_data"])}</span>
    </div>
  </header>

  <section>
    <h2>{e(t["h_prima"])}</h2>
    <div class="g-griglia">
      {scheda(t["s1_t"], t["s1_p"])}
      {scheda(t["s2_t"], t["s2_p"])}
      {scheda(t["s3_t"], t["s3_p"])}
    </div>
  </section>

  <section>
    <h2>{e(t["h_tre"])}</h2>
    <p>{t["tre_p"]}</p>
    <div class="g-tabella">
      <table>
        <thead><tr>
          <th>{e(t["th_modo"])}</th><th>{e(t["th_quando"])}</th>
          <th>{e(t["th_chi"])}</th><th>{e(t["th_porta"])}</th><th>{e(t["th_aprire"])}</th>
        </tr></thead>
        <tbody>
          <tr><th>{e(t["lan"])}</th><td>{e(t["lan_q"])}</td><td>{e(t["lan_c"])}</td>
              <td class="num">5555</td><td>{e(t["lan_a"])}</td></tr>
          <tr><th>{e(t["relay"])}</th><td>{e(t["relay_q"])}</td><td>{e(t["relay_c"])}</td>
              <td class="num">5555</td><td>{e(t["relay_a"])}</td></tr>
          <tr><th>{e(t["casa"])}</th><td>{e(t["casa_q"])}</td><td>{e(t["casa_c"])}</td>
              <td class="num">5555</td><td>{e(t["casa_a"])}</td></tr>
        </tbody>
      </table>
    </div>
    <p>{t["tre_fine"]}</p>
  </section>

  <section>
    <h2>{e(t["h_pa"])}</h2>

    <div class="g-percorso">
      <div class="g-intestazione">
        <span class="g-sigla">{e(t["pa1_sigla"])}</span>
        <h3>{e(t["pa1_h3"])}</h3>
      </div>
      <ol class="g-passi">
        {passo(t["pa1_1"], t["pa1_1n"])}
        {passo(t["pa1_2"])}
        {passo(t["pa1_3"], t["pa1_3n"])}
        {passo(t["pa1_4"])}
        {passo(t["pa1_5"])}
      </ol>
    </div>

    <div class="g-percorso">
      <div class="g-intestazione">
        <span class="g-sigla">{e(t["pa2_sigla"])}</span>
        <h3>{e(t["pa2_h3"])}</h3>
      </div>
      <ol class="g-passi">
        {passo(t["pa2_1"], t["pa2_1n"])}
        {passo(t["pa2_2"])}
        {passo(t["pa2_3"])}
        {passo(t["pa2_4"])}
      </ol>
    </div>

    <div class="g-avviso">
      <strong>{e(t["pa_avv_t"])}</strong>
      <p>{t["pa_avv_p"]}</p>
    </div>
  </section>

  <section>
    <h2>{e(t["h_pb"])}</h2>

    <div class="g-percorso">
      <div class="g-intestazione">
        <span class="g-sigla">{e(t["pb1_sigla"])}</span>
        <h3>{e(t["pb1_h3"])}</h3>
      </div>
      <ol class="g-passi">
        {passo(t["pb1_1"])}
        {passo(t["pb1_2"])}
        {passo(t["pb1_3"], t["pb1_3n"])}
      </ol>
      <dl class="g-campi">
        <dt>{e(t["ruolo_tit"])}</dt><dd>{t["ruolo_tit_d"]}</dd>
        <dt>{e(t["ruolo_op"])}</dt><dd>{t["ruolo_op_d"]}</dd>
        <dt>{e(t["ruolo_asc"])}</dt><dd>{t["ruolo_asc_d"]}</dd>
      </dl>
    </div>

    <div class="g-percorso">
      <div class="g-intestazione">
        <span class="g-sigla">{e(t["pb2_sigla"])}</span>
        <h3>{e(t["pb2_h3"])}</h3>
      </div>
      <ol class="g-passi">
        {passo(t["pb2_1"], t["pb2_1n"])}
        {passo(t["pb2_2"])}
        {passo(t["pb2_3"])}
        {passo(t["pb2_4"], t["pb2_4n"])}
        {passo(t["pb2_5"])}
      </ol>
    </div>

    <div class="g-percorso">
      <div class="g-intestazione">
        <span class="g-sigla">{e(t["pb3_sigla"])}</span>
        <h3>{e(t["pb3_h3"])}</h3>
      </div>
      <ol class="g-passi">
        {passo(t["pb3_1"])}
        {passo(t["pb3_2"])}
        {passo(t["pb3_3"], t["pb3_3n"])}
        {passo(t["pb3_4"])}
      </ol>
      <dl class="g-campi">
        <dt>{e(t["campi_acc"])}</dt><dd>decolink.ft2.it</dd>
        <dt>{e(t["campi_email"])}</dt><dd><span class="libero">{e(t["campi_email_d"])}</span></dd>
        <dt>{e(t["campi_pw"])}</dt><dd><span class="libero">{e(t["campi_pw_d"])}</span></dd>
        <dt>{e(t["campi_relay"])}</dt><dd><span class="libero">{e(t["campi_relay_d"])}</span></dd>
        <dt>{e(t["campi_porta"])}</dt><dd>5555</dd>
      </dl>
    </div>

    <div class="g-avviso">
      <strong>{e(t["pb_avv_t"])}</strong>
      <p>{t["pb_avv_p"]}</p>
    </div>
  </section>

  <section>
    <h2>{e(t["h_pc"])}</h2>
    <p>{e(t["pc_p"])}</p>
    <div class="g-percorso">
      <ol class="g-passi">
        {passo(t["pc_1"])}
        {passo(t["pc_2"])}
        {passo(t["pc_3"])}
      </ol>
    </div>
    <p>{t["pc_fine"]}</p>
  </section>

  <section>
    <h2>{e(t["h_cat"])}</h2>
    <p>{e(t["cat_p"])}</p>
    <div class="g-tabella">
      <table>
        <thead><tr>
          <th>{e(t["cat_th1"])}</th><th>{e(t["cat_th2"])}</th><th>{e(t["cat_th3"])}</th>
        </tr></thead>
        <tbody>
          <tr><th>{e(t["cat_r1"])}</th><td>{t["cat_r1d"]}</td><td>{e(t["cat_r1w"])}</td></tr>
          <tr><th>{e(t["cat_r2"])}</th><td>{e(t["cat_r2d"])}</td><td>{e(t["cat_r2w"])}</td></tr>
          <tr><th>{e(t["cat_r3"])}</th><td>{e(t["cat_r3d"])}</td><td>{e(t["cat_r3w"])}</td></tr>
        </tbody>
      </table>
    </div>
    <p>{t["cat_fine"]}</p>
  </section>

  <section>
    <h2>{e(t["h_guai"])}</h2>
    <div class="g-sintomi">
      {sintomo(t["g1_m"], t["g1_c"])}
      {sintomo(t["g2_m"], t["g2_c"])}
      {sintomo(t["g3_m"], t["g3_c"])}
      {sintomo(t["g4_m"], t["g4_c"])}
      {sintomo(t["g5_m"], t["g5_c"])}
      {sintomo(t["g6_m"], t["g6_c"])}
    </div>
  </section>

  <section>
    <h2>{e(t["h_demo"])}</h2>
    <p>{t["demo_p"]}</p>
  </section>

  <footer class="g-piede">{e(t["piede"])}</footer>
</div>"""
