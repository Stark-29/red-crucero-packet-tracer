# Cableado y descriptions

Tabla de conexiones entre equipos (obtenida con `show cdp neighbors`) y las `description` de cada interfaz.

- Los PCs, teléfonos con PC detrás y servidores no aparecen siempre en CDP; sus puertos se documentan aparte.

---

## 1. Tabla de cableado

### Internet simulado

| Equipo A | Puerto A | Equipo B | Puerto B | Medio | Red |
|---|---|---|---|---|---|
| SAT-A | Gi0/0 | SW-ISP | Gi0/1 | Cobre | 203.0.113.0/24 |
| SAT-B | Gi0/0 | SW-ISP | Gi0/2 | Cobre | 203.0.113.0/24 |
| SRV-INTERNET | NIC | SW-ISP | Fa0/1 | Cobre | 203.0.113.0/24 |
| SAT-A | Gi0/1 | EDGE-R1 | Gi0/0/0 | Cobre | 198.51.100.0/30 |
| SAT-B | Gi0/1 | EDGE-R2 | Gi0/0/0 | Cobre | 198.51.100.4/30 |

### Edge ↔ Core (enrutados)

| Equipo A | Puerto A | Equipo B | Puerto B | Medio | Red |
|---|---|---|---|---|---|
| EDGE-R1 | Gi0/0/1 | CORE-SW1 | Gi1/0/1 | Cobre | 10.255.1.0/30 |
| EDGE-R1 | Gi0/0/2 | CORE-SW2 | Gi1/0/2 | Cobre | 10.255.1.4/30 |
| EDGE-R2 | Gi0/0/2 | CORE-SW1 | Gi1/0/2 | Cobre | 10.255.1.8/30 |
| EDGE-R2 | Gi0/0/1 | CORE-SW2 | Gi1/0/1 | Cobre | 10.255.1.12/30 |

### Core ↔ Core (Port-channel 10, LACP capa 3)

| Equipo A | Puerto A | Equipo B | Puerto B | Medio | Red |
|---|---|---|---|---|---|
| CORE-SW1 | Gi1/0/3 | CORE-SW2 | Gi1/0/3 | Cobre | 10.255.2.0/30 |
| CORE-SW1 | Gi1/0/4 | CORE-SW2 | Gi1/0/4 | Cobre | 10.255.2.0/30 |

### Core ↔ Distribution (fibra monomodo, enrutados)

| Equipo A | Puerto A | Equipo B | Puerto B | Medio | Red |
|---|---|---|---|---|---|
| CORE-SW1 | Gi1/1/1 | DIST-SW1 | Gi1/1/1 | Fibra | 10.255.3.0/30 |
| CORE-SW1 | Gi1/1/2 | DIST-SW2 | Gi1/1/2 | Fibra | 10.255.3.4/30 |
| CORE-SW2 | Gi1/1/2 | DIST-SW1 | Gi1/1/2 | Fibra | 10.255.3.8/30 |
| CORE-SW2 | Gi1/1/1 | DIST-SW2 | Gi1/1/1 | Fibra | 10.255.3.12/30 |

### Distribution ↔ Distribution (Port-channel 1, LACP capa 2, trunk)

| Equipo A | Puerto A | Equipo B | Puerto B | Medio |
|---|---|---|---|---|
| DIST-SW1 | Gi1/0/5 | DIST-SW2 | Gi1/0/5 | Cobre |
| DIST-SW1 | Gi1/0/6 | DIST-SW2 | Gi1/0/6 | Cobre |


### Distribution ↔ Access y Data Center (trunks)

| Equipo A | Puerto A | Equipo B | Puerto B |
|---|---|---|---|
| DIST-SW1 | Gi1/0/1 | ACC-CREW | Gi0/1 |
| DIST-SW2 | Gi1/0/1 | ACC-CREW | Gi0/2 |
| DIST-SW1 | Gi1/0/2 | ACC-GUEST | Gi0/1 |
| DIST-SW2 | Gi1/0/2 | ACC-GUEST | Gi0/2 |
| DIST-SW1 | Gi1/0/3 | ACC-BRIDGE | Gi0/1 |
| DIST-SW2 | Gi1/0/3 | ACC-BRIDGE | Gi0/2 |
| DIST-SW1 | Gi1/0/4 | SW-DC | Gi0/1 |
| DIST-SW2 | Gi1/0/4 | SW-DC | Gi0/2 |

### Data Center

| Equipo A | Puerto A | Equipo B | Puerto B |
|---|---|---|---|
| SW-DC | Fa0/1 | SRV-INFRA | NIC |
| SW-DC | Fa0/2 | R-VOZ | Gi0/0 |
| SW-DC | Fa0/3 | SRV-WEB | NIC |

### Puertos de usuario (Access)

| Switch | Puertos | Equipo | VLAN |
|---|---|---|---|
| ACC-CREW | Fa0/1, Fa0/2 | Teléfono IP + PC detrás | 10 (datos) / 40 (voz) |
| ACC-CREW | Fa0/3 | PC | 10 |
| ACC-CREW | Fa0/4 | PC del administrador de TI | 30 |
| ACC-GUEST | Fa0/1 | Teléfono IP + PC detrás | 20 (datos) / 40 (voz) |
| ACC-GUEST | Fa0/2 - Fa0/3 | PC | 20 |
| ACC-BRIDGE | Fa0/1 | Teléfono IP + PC detrás | 60 (datos) / 40 (voz) |
| ACC-BRIDGE | Fa0/2 - Fa0/3 | PC | 60 |

---

## 2. Estándar de descriptions

Texto en ASCII (sin tildes ni caracteres especiales), en mayúsculas para el tipo de enlace y siempre con el equipo y puerto del otro extremo.

| Tipo | Formato | Ejemplo |
|---|---|---|
| Trunk L2 | `TRUNK to <equipo> <puerto>` | `TRUNK to DIST-SW1 Gi1/0/1` |
| Enlace enrutado | `P2P to <equipo> <puerto> <red>` | `P2P to CORE-SW1 Gi1/0/1 10.255.1.0/30` |
| WAN | `WAN to <equipo> <puerto> <red>` | `WAN to SAT-A Gi0/1 198.51.100.0/30` |
| EtherChannel | `LACP Po<n> to <equipo> <puerto>` | `LACP Po1 to DIST-SW2 Gi1/0/5` |
| PC | `PC-<grupo>-<n> VLAN<n>` | `PC-CREW-3 VLAN10` |
| Teléfono + PC | `PHONE-<grupo>-<n> + PC-<grupo>-<n>` | `PHONE-CREW-1 + PC-CREW-1` |
| Servidor | `<nombre> <IP>` | `SRV-INFRA 10.0.50.10` |
| SVI | `GW <grupo> (HSRP VIP <IP>)` | `GW CREW (HSRP VIP 10.0.10.1)` |
| Sin uso | `UNUSED - shutdown` | |

## 3. Descriptions por equipo

### SAT-A

```
interface GigabitEthernet0/0
 description LAN to SW-ISP Gi0/1 203.0.113.0/24
interface GigabitEthernet0/1
 description WAN to EDGE-R1 Gi0/0/0 198.51.100.0/30
```

### SAT-B

```
interface GigabitEthernet0/0
 description LAN to SW-ISP Gi0/2 203.0.113.0/24
interface GigabitEthernet0/1
 description WAN to EDGE-R2 Gi0/0/0 198.51.100.4/30
```

### SW-ISP

```
interface GigabitEthernet0/1
 description LAN to SAT-A Gi0/0
interface GigabitEthernet0/2
 description LAN to SAT-B Gi0/0
interface FastEthernet0/1
 description SRV-INTERNET 203.0.113.10
```

### EDGE-R1

```
interface Loopback0
 description ROUTER-ID OSPF
interface GigabitEthernet0/0/0
 description WAN to SAT-A Gi0/1 198.51.100.0/30
interface GigabitEthernet0/0/1
 description P2P to CORE-SW1 Gi1/0/1 10.255.1.0/30
interface GigabitEthernet0/0/2
 description P2P to CORE-SW2 Gi1/0/2 10.255.1.4/30
```

### EDGE-R2

```
interface Loopback0
 description ROUTER-ID OSPF
interface GigabitEthernet0/0/0
 description WAN to SAT-B Gi0/1 198.51.100.4/30
interface GigabitEthernet0/0/1
 description P2P to CORE-SW2 Gi1/0/1 10.255.1.12/30
interface GigabitEthernet0/0/2
 description P2P to CORE-SW1 Gi1/0/2 10.255.1.8/30
```

### CORE-SW1

```
interface Loopback0
 description ROUTER-ID OSPF
interface GigabitEthernet1/0/1
 description P2P to EDGE-R1 Gi0/0/1 10.255.1.0/30
interface GigabitEthernet1/0/2
 description P2P to EDGE-R2 Gi0/0/2 10.255.1.8/30
interface range GigabitEthernet1/0/3 - 4
 description LACP Po10 to CORE-SW2 Gi1/0/3-4
interface Port-channel10
 description P2P LACP to CORE-SW2 Po10 10.255.2.0/30
interface GigabitEthernet1/1/1
 description P2P to DIST-SW1 Gi1/1/1 10.255.3.0/30
interface GigabitEthernet1/1/2
 description P2P to DIST-SW2 Gi1/1/2 10.255.3.4/30
```

### CORE-SW2

```
interface Loopback0
 description ROUTER-ID OSPF
interface GigabitEthernet1/0/1
 description P2P to EDGE-R2 Gi0/0/1 10.255.1.12/30
interface GigabitEthernet1/0/2
 description P2P to EDGE-R1 Gi0/0/2 10.255.1.4/30
interface range GigabitEthernet1/0/3 - 4
 description LACP Po10 to CORE-SW1 Gi1/0/3-4
interface Port-channel10
 description P2P LACP to CORE-SW1 Po10 10.255.2.0/30
interface GigabitEthernet1/1/1
 description P2P to DIST-SW2 Gi1/1/1 10.255.3.12/30
interface GigabitEthernet1/1/2
 description P2P to DIST-SW1 Gi1/1/2 10.255.3.8/30
```

### DIST-SW1

```
interface Loopback0
 description ROUTER-ID OSPF
interface GigabitEthernet1/1/1
 description P2P to CORE-SW1 Gi1/1/1 10.255.3.0/30
interface GigabitEthernet1/1/2
 description P2P to CORE-SW2 Gi1/1/2 10.255.3.8/30
interface GigabitEthernet1/0/1
 description TRUNK to ACC-CREW Gi0/1
interface GigabitEthernet1/0/2
 description TRUNK to ACC-GUEST Gi0/1
interface GigabitEthernet1/0/3
 description TRUNK to ACC-BRIDGE Gi0/1
interface GigabitEthernet1/0/4
 description TRUNK to SW-DC Gi0/1
interface range GigabitEthernet1/0/5 - 6
 description LACP Po1 to DIST-SW2 Gi1/0/5-6
interface Port-channel1
 description TRUNK LACP to DIST-SW2 Po1
interface Vlan10
 description GW CREW (HSRP VIP 10.0.10.1)
interface Vlan20
 description GW GUESTS (HSRP VIP 10.0.20.1)
interface Vlan30
 description GW ADMIN-IT (HSRP VIP 10.0.30.1)
interface Vlan40
 description GW VOICE (HSRP VIP 10.0.40.1)
interface Vlan50
 description GW SERVERS (HSRP VIP 10.0.50.1)
interface Vlan60
 description GW BRIDGE-OPS (HSRP VIP 10.0.60.1)
interface Vlan100
 description GW MGMT (HSRP VIP 10.0.100.1)
```

### DIST-SW2

```
interface Loopback0
 description ROUTER-ID OSPF
interface GigabitEthernet1/1/1
 description P2P to CORE-SW2 Gi1/1/1 10.255.3.12/30
interface GigabitEthernet1/1/2
 description P2P to CORE-SW1 Gi1/1/2 10.255.3.4/30
interface GigabitEthernet1/0/1
 description TRUNK to ACC-CREW Gi0/2
interface GigabitEthernet1/0/2
 description TRUNK to ACC-GUEST Gi0/2
interface GigabitEthernet1/0/3
 description TRUNK to ACC-BRIDGE Gi0/2
interface GigabitEthernet1/0/4
 description TRUNK to SW-DC Gi0/2
interface range GigabitEthernet1/0/5 - 6
 description LACP Po1 to DIST-SW1 Gi1/0/5-6
interface Port-channel1
 description TRUNK LACP to DIST-SW1 Po1
interface Vlan10
 description GW CREW (HSRP VIP 10.0.10.1)
interface Vlan20
 description GW GUESTS (HSRP VIP 10.0.20.1)
interface Vlan30
 description GW ADMIN-IT (HSRP VIP 10.0.30.1)
interface Vlan40
 description GW VOICE (HSRP VIP 10.0.40.1)
interface Vlan50
 description GW SERVERS (HSRP VIP 10.0.50.1)
interface Vlan60
 description GW BRIDGE-OPS (HSRP VIP 10.0.60.1)
interface Vlan100
 description GW MGMT (HSRP VIP 10.0.100.1)
```

### ACC-CREW

```
interface GigabitEthernet0/1
 description TRUNK to DIST-SW1 Gi1/0/1
interface GigabitEthernet0/2
 description TRUNK to DIST-SW2 Gi1/0/1
interface FastEthernet0/1
 description PHONE-CREW-1 + PC-CREW-1
interface FastEthernet0/2
 description PHONE-CREW-2 + PC-CREW-2
interface FastEthernet0/3
 description PC-CREW-3 VLAN10
interface FastEthernet0/4
 description PC-ADMIN-1 VLAN30
interface Vlan100
 description MGMT ACC-CREW
```

### ACC-GUEST

```
interface GigabitEthernet0/1
 description TRUNK to DIST-SW1 Gi1/0/2
interface GigabitEthernet0/2
 description TRUNK to DIST-SW2 Gi1/0/2
interface FastEthernet0/1
 description PHONE-GUEST-1 + PC-GUEST-1
interface FastEthernet0/2
 description PC-GUEST-2 VLAN20
interface FastEthernet0/3
 description PC-GUEST-3 VLAN20
interface Vlan100
 description MGMT ACC-GUEST
```

### ACC-BRIDGE

```
interface GigabitEthernet0/1
 description TRUNK to DIST-SW1 Gi1/0/3
interface GigabitEthernet0/2
 description TRUNK to DIST-SW2 Gi1/0/3
interface FastEthernet0/1
 description PHONE-BRIDGE-1 + PC-BRIDGE-1
interface FastEthernet0/2
 description PC-BRIDGE-2 VLAN60
interface FastEthernet0/3
 description PC-BRIDGE-3 VLAN60
interface Vlan100
 description MGMT ACC-BRIDGE
```

### SW-DC

```
interface GigabitEthernet0/1
 description TRUNK to DIST-SW1 Gi1/0/4
interface GigabitEthernet0/2
 description TRUNK to DIST-SW2 Gi1/0/4
interface FastEthernet0/1
 description SRV-INFRA 10.0.50.10
interface FastEthernet0/2
 description R-VOZ 10.0.50.5
interface FastEthernet0/3
 description SRV-WEB 10.0.50.20
interface Vlan100
 description MGMT SW-DC
```

### R-VOZ

```
interface GigabitEthernet0/0
 description LAN to SW-DC Fa0/2 VLAN50 10.0.50.5
```

### Puertos sin uso

```
! ACC-GUEST, ACC-BRIDGE y SW-DC
interface range FastEthernet0/4 - 24
 description UNUSED - shutdown

! ACC-CREW (Fa0/4 lo usa PC-ADMIN)
interface range FastEthernet0/5 - 24
 description UNUSED - shutdown

! SW-ISP
interface range FastEthernet0/2 - 24
 description UNUSED - shutdown
 
! DIST-SW1 y DIST-SW2
interface range GigabitEthernet1/0/7 - 24
 description UNUSED - shutdown
interface range GigabitEthernet1/1/3 - 4
 description UNUSED - shutdown

! CORE-SW1 y CORE-SW2
interface range GigabitEthernet1/0/5 - 24
 description UNUSED - shutdown
interface range GigabitEthernet1/1/3 - 4
 description UNUSED - shutdown
```

Estos puertos, además, están en `shutdown` (y en la VLAN 999 donde hay puertos de acceso); ver los archivos de `configs/`.

---
