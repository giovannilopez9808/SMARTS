# SMARTS model

## Requeriments

```bash
scipy==1.7.3
pandas==1.3.5
numpy==1.21.5
tqdm==4.62.3
```

## Output compilation

```bash
gfortran -O3 -g -o smarts.out smarts.f
smarts.f:1523:72:

1523 | IF(EPSI) 20,5,8
| 1
Warning: Fortran 2018 deleted feature: Arithmetic IF statement at (1)
smarts.f:1529:72:

1529 | IF(EPSI) 7,5,20
| 1
Warning: Fortran 2018 deleted feature: Arithmetic IF statement at (1)
mv smarts.out ../
```
