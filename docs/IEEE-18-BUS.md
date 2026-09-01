# IEEE 18-Bus System — Data Source

## Source

The IEEE 18-bus radial distribution system used in this project
is based on the test system reported in:

> M. Milovanović, J. Radosavljević, B. Perović, and M. Dragičević,
> "Power flow in radial distribution systems in the presence of
> harmonics," _International Journal of Electrical Engineering
> and Computing_, vol. 2, no. 1, 2018.

The IEEE 18-bus system data are provided in Appendix A, Table A.I.

## System Base

| Parameter     |     Value |
| ------------- | --------: |
| Base Power    |    10 MVA |
| Base Voltage  |   12.5 kV |
| Frequency     |     50 Hz |
| Slack Bus     |         1 |
| Slack Voltage | 1.05 p.u. |

## Bus Numbering

The original system uses the following 18 bus identifiers:

```text
1, 2, 3, 4, 5, 6, 7, 8, 9,
20, 21, 22, 23, 24, 25, 26, 50, 51
```

The non-consecutive numbering is intentionally preserved.

## Network Data

The line parameters in `system_data.py` are based on
Appendix A, Table A.I of the cited paper.

The system contains two parallel branches between buses 25 and 26.
Both branches are retained.

## Nonlinear Load

A six-pulse converter is connected at bus 5.

```text
P = 0.300 p.u.
Q = 0.226 p.u.
```

On the 10 MVA base:

```text
P = 3.00 MW
Q = 2.26 MVAr
```

## Citation

```bibtex
@article{milovanovic2018,
  author  = {Milovanović, M. and Radosavljević, J. and Perović, B. and Dragičević, M.},
  title   = {Power flow in radial distribution systems in the presence of harmonics},
  journal = {International Journal of Electrical Engineering and Computing},
  volume  = {2},
  number  = {1},
  year    = {2018}
}
```

## Original Reference

The IEEE 18-bus test system originates from the work of:

> W. M. Grady, M. J. Samotyj, and A. H. Noyola,
> "The application of network objective functions for actively
> minimizing the impact of voltage harmonics in power systems,"
> _IEEE Transactions on Power Delivery_, vol. 7,
> pp. 1379–1386, July 1992.
