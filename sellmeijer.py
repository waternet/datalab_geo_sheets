#!/usr/bin/python

import math

class Sellmeijer:
    def __init__(self):
        """This class represents a Sellmeijer based piping calculation.
        Use the class to set all the parameters and use calc to find the result
        of the calculation. The mandatory parameters *need to be set* before
        a calculation can be made.

        This class stores the report of the calculation which can be accessed by
        using the save_report function

        Mandatory parameters (variable name, meaning, unit):
        ---------------------------------------------------------------------
        boezempeil          boezempeil                              m tov NAP
        slootpeil           slootpeil                               m tov NAP
        d                   dikte slappe lagen pakket               m
        d70_m               referentie d70 waarde                   m
        L                   kwelweglengte                           m
        d70                 70percentielwaarde korrelverdeling      m
        D                   dikte zandlaag                          m
        gamma_b             schematiseringsfactor                   -
        k                   doorlatendheid                          m/s

        Optional parameters (variable name (default), meaning, unit):
        eta (0.25)          sleepkrachtfactor                       -
        gamma_p (16.50)     volumegewicht zandkorrels               kN/m3
        gamma_w (9.81)      volumegewicht water                     kN/m3
        theta (37.)         rolweerstandshoek zandkorrels           graden
        tn95 (1.65)         t waarde verzameling                    -
        Vc_d (0.1)          statistische verdeling voor d           -
        Vc_L (0.1)          statistische verdeling voor L           -
        Vc_d70 (0.25)       statistische verdeling voor d70         -
        Vc_D (0.1)          statistische verdeling voor D           -
        Vc_kappa (0.1)      statistische verdeling voor kappa       -

        For examples on usage see test_sellmeijer.py
        """

        self.boezempeil = 0.0
        self.slootpeil = 0.0
        self.d = 0.
        self.d70_m= 0.
        self.L = 0.
        self.d70 = 0.
        self.D = 0.
        self.gamma_b = 0.
        self.k = 0.

        #default values
        self.eta = 0.25
        self.gamma_p = 16.50
        self.gamma_w = 9.81
        self.theta = 37.
        self.tn95 = 1.65
        self.Vc_d = 0.1
        self.Vc_L = 0.1
        self.Vc_d70 = 0.25
        self.Vc_D = 0.1
        self.Vc_kappa = 0.1

        self._report = ""

    def _calc_kappa(self, k):
        """This is a helper function to calculate an intermediate value"""
        #kinematische viscositeit van water
        ypsilon_water = 1.33e-6
        #zwaartekrachtversnelling
        g = 9.81
        #geef intrinsieke doorlatendheid terug
        return (ypsilon_water / g) * k

    def _report_invoer(self, normklasse, rep):
        """This is a helper function to generate parts of the report output"""
        self._report += """<h2>Sellmeijer piping berekening</h2>"""

        nk_txt = "1/10 - 1/100"
        if normklasse==2:
            nk_txt = "1/300 - 1/1000"

        rep_txt = "normale parameters"
        if rep:
            rep_txt = "representatieve parameters"

        self._report += """<p>Deze berekening kijkt naar de pipingveiligheid gebaseerd op normklasse %s en %s.</p>""" % (nk_txt, rep_txt)
        self._report += """<p><h4>Invoer parameters</h4>"""
        self._report += """<table border="0" width="100%"><tr><th width="50%" align="left">Parameter</th><th width="40%" align="left">Waarde</th><th width="40%" align="left">Eenheid</th></tr>"""
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("boezempeil", self.boezempeil, "m NAP")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("slootpeil", self.slootpeil, "m NAP")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("dikte slappe lagen pakket", self.d, "m")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("sleepkrachtfactor", self.eta, "-")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("volume gewicht zandkorrels", self.gamma_p, "kN/m3")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("volumegewicht water", self.gamma_w, "kN/m3")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("rolweerstandshoek zandkorrels", self.theta, "graden")
        self._report += """<tr><td>%s</td><td>%.2e</td><td>%s</td></tr>""" % ("referentie d70 waarde", self.d70_m, "m")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("kwelweglengte", self.L, "m")
        self._report += """<tr><td>%s</td><td>%.2e</td><td>%s</td></tr>""" % ("70percentielwaarde korrelverdeling", self.d70, "m")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("dikte zandlaag", self.D, "m")
        self._report += """<tr><td>%s</td><td>%.2e</td><td>%s</td></tr>""" % ("doorlatendheid", self.k, "m/s")
        self._report += """</table>"""

    def _report_conclusie(self, deklaagdikte, normklasse, rep, conclusie):
        """This is a helper function to write assessment outcome text"""
        nk_txt = "1/10 - 1/100"
        if normklasse==2:
            nk_txt = "1/300 - 1/1000"

        rep_txt = "normale parameters"
        if rep:
            rep_txt = "representatieve parameters"

        con_txt = "voldoet niet"
        if conclusie:
            con_txt = "voldoet"

        self._report += """<p>Bij een deklaagdikte van %.2fm, een normklasse %s en %s is het oordeel <b>%s</b></p>""" % (deklaagdikte, nk_txt, rep_txt, con_txt)

    def calc_from_params(self, boezempeil, slootpeil, d, d70_m, L, d70, D, gamma_b, k, deklaagdikte, normklasse, rep):
        """This function is used for automated calls. The following mandatory
        parameters need to be passed to this function

        boezempeil          boezempeil                              m tov NAP
        slootpeil           slootpeil                               m tov NAP
        d                   dikte slappe lagen pakket               m
        d70_m               referentie d70 waarde                   m
        L                   kwelweglengte                           m
        d70                 70percentielwaarde korrelverdeling      m
        D                   dikte zandlaag                          m
        gamma_b             schematiseringsfactor                   -
        k                   doorlatendheid                          m/s
        deklaagdikte        dikte van de deklaag                    m
        normklasse          1=(1/10-1/100), 2=(1/300-1/1000)        -
        rep                 use representative parameters           True/False
        """
        self.boezempeil = boezempeil
        self.slootpeil = slootpeil
        self.d = d
        self.d70_m = d70_m
        self.L = L
        self.d70 = d70
        self.D = D
        self.gamma_b = gamma_b
        self.k = k
        return self.calc(deklaagdikte, normklasse, rep)

    def calc(self, deklaagdikte, normklasse=2, rep=True):
        """This function calculates the piping sensivity according to the Sellmeijer method.

        Input
        Parameter       meaning                             unit            default
        ---------------------------------------------------------------------------
        deklaagdikte    dikte van de deklaag                m
        normklasse      1=(1/10-1/100), 2=(1/300-1/1000)    -               2
        rep             use representative parameters       True/False      True

        Output:
        Assessment judgement (True = safe, False = not safe)
        """
        self._report_invoer(normklasse, rep)

        self._report += """<h4>Berekende parameters</h4>"""
        self._report += """<table border="0" width="100%"><tr><th width="50%" align="left">Parameter</th><th width="40%" align="left">Waarde</th><th width="40%" align="left">Eenheid</th></tr>"""

        kappa = self._calc_kappa(self.k)
        self._report += """<tr><td>%s</td><td>%.2e</td><td>%s</td></tr>""" % ("intrinsieke doorlatendheid zandlaag", kappa, "m2")

        if rep:
            d_rep = self.d * (1-self.Vc_d * self.tn95)
            L_rep = self.L * (1-self.Vc_L * self.tn95)
            d70_rep = self.d70 * (1-self.Vc_d70 * self.tn95)
            D_rep = self.D * (1+self.Vc_D * self.tn95)
            kappa_rep = kappa * (1+self.Vc_kappa * self.tn95)

            self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("dikte slappe lagen pakket (repr waarde)", d_rep, "m2")
            self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("kwelweglengte (repr waarde)", L_rep, "m")
            self._report += """<tr><td>%s</td><td>%.2e</td><td>%s</td></tr>""" % ("70percentielwaarde korrelverdeling (repr waarde)", d70_rep, "m")
            self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("dikte zandlaag (repr waarde)", D_rep, "m")
            self._report += """<tr><td>%s</td><td>%.2e</td><td>%s</td></tr>""" % ("intrinsieke doorlatendheid zandlaag (repr waarde)", kappa_rep, "m2")


        F_resistance = self.eta * (self.gamma_p / self.gamma_w) * math.tan(math.radians(self.theta))

        F_scale = self.d70_m / math.pow(kappa * self.L, 1/3.) * math.pow(self.d70 / self.d70_m, 0.4)
        F_geometry = 0.91 * math.pow((self.D / self.L), (0.28 / ((math.pow(self.D / self.L, 2.8) - 1.)) + 0.04))
        if rep:
            F_scale = self.d70_m / math.pow(kappa_rep * L_rep, 1/3.) * math.pow(d70_rep / self.d70_m, 0.4)
            F_geometry = 0.91 * math.pow((D_rep / L_rep), (0.28 / ((math.pow(D_rep / L_rep, 2.8) - 1.)) + 0.04))

        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("F;resistance", F_resistance, "-")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("F;scale", F_scale, "-")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("F;geometry", F_geometry, "-")


        delta_Hc = F_resistance * F_scale * F_geometry * self.L
        if rep:
            delta_Hc = F_resistance * F_scale * F_geometry * L_rep



        H = self.boezempeil - self.slootpeil

        delta_H03d = H - (0.3*self.d)
        if rep:
            delta_H03d = H - (0.3*d_rep)


        gamma = delta_Hc / (delta_H03d * self.gamma_b)

        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("kritisch verval", delta_Hc, "m")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("verval met 0.3 regel", delta_H03d, "m")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("werkelijk verval", H, "m")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("schematiseringsfactor", self.gamma_b, "-")
        self._report += """<tr><td>%s</td><td>%.2f</td><td>%s</td></tr>""" % ("veiligheidsfactor", gamma, "-")

        self._report += """</table></p>"""

        if deklaagdikte<2:
            if normklasse==1:
                self._report_conclusie(deklaagdikte, normklasse, rep, gamma >= 1.2)
                return gamma >= 1.2
            if normklasse==2:
                self._report_conclusie(deklaagdikte, normklasse, rep, gamma >= 1.4)
                return gamma >= 1.4
        else:
            if normklasse==1:
                self._report_conclusie(deklaagdikte, normklasse, rep, gamma >= 1.1)
                return gamma >= 1.1
            if normklasse==2:
                self._report_conclusie(deklaagdikte, normklasse, rep, gamma >= 1.3)
                return gamma >= 1.3

        return false

    def save_report(self, filename):
        """This function saves the report of the last calculation."""
        import fpdf

        class MyFPDF(fpdf.FPDF, fpdf.HTMLMixin):
            pass

        pdf=MyFPDF()
        pdf.add_page()
        pdf.write_html(self._report)
        pdf.output(filename,'F')

def domino_calc(boezempeil, slootpeil, d, d70_m, L, d70, D, gamma_b, k, deklaagdikte, normklasse, rep):
    """Helper function to enable API point calls to the Sellmeijer calculations.
    For parameters see Sellmeijer.calc_from_params function"""
    S = Sellmeijer()
    return S.calc_from_params(boezempeil, slootpeil, d, d70_m, L, d70, D, gamma_b, k, deklaagdikte, normklasse, rep)
