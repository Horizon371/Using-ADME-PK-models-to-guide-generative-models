<b>Thesis</b>: https://www.diva-portal.org/smash/record.jsf?pid=diva2%3A1875004&dswid=-9882

<h3>Abstract</h3>

An adequate ADME/PK (absorption, distribution, metabolism, excretion, pharmacokinetics) profile is an essential quality for a drug. As part of the drug discovery process,
leads are iteratively designed and optimized in order to simultaneously satisfy various
properties such as appropriate ADME/PK levels and high biological activity for a target.
The drug discovery process can be accelerated by improving the likelihood that a designed
compound fulfils the necessary pharmacologic properties, and thus reducing the number
of needed iterations. A promising technique is de novo drug design, where molecules are
computationally generated based on a set of desired attributes.

Our project aimed to benchmark the effectiveness of the ANDROMEDA ADME/PK
conformal prediction models in guiding the generation of compounds toward an area of
chemical space with good ADME/PK properties. For this, we used the REINVENT
reinforcement learning framework built by the Molecular AI team at AstraZeneca. Here,
we integrated 4 out the 14 available ANDROMEDA models (fabs , fdiss, CLint and Vss) as
oracles in the scoring component of the generative model. Oral bioavailability (F) is a
secondary parameter that was computed with the help of the aforementioned models and
fu (unbound fraction in plasma), and serves as the fifth ADME/PK oracle in our analysis.
We aimed to rediscover DRD2 bioactives with a good ADME/PK profile.

Our results show that the ANDROMEDA models have a slight influence on the predicted
ADME/PK properties of the generated compounds. The results do not show an increased likelihood of generating DRD2 ligands in the case of the primary ANDROMEDA
models. However, when using the oral bioavailability oracle, the sampling likelihood increases for some of the approved DRD2 ligands. In conclusion, the oral bioavailability
ANDROMEDA model can be a promising option for guiding the generation of novel
compounds towards an area of chemical space with good ADME/PK properties.
