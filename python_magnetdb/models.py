from typing import List, Optional

from fastapi import FastAPI
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

class MaterialBase(SQLModel):
    """
    Material Physical Properties in SI for isotropic material
    """
    
    name: str

    Tref: float

    VolumicMass: float
    SpecificHeat: float

    alpha: Optional[float] = 0
    ElectricalConductivity: Optional[float] = 0
    ThermalConductivity: float
    MagnetPermeability: float

    Young: float
    Poisson: float
    CoefDilatation: float
    
    ref: Optional[str] = None

class Material(MaterialBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class MaterialCreate(MaterialBase):
    pass

class MaterialRead(MaterialBase):
    id: int

class MaterialUpdate(SQLModel):
    name: str

    Tref: float

    VolumicMass: float
    SpecificHeat: float

    alpha: Optional[float] = 0
    ElectricalConductivity: Optional[float] = 0
    ThermalConductivity: float
    MagnetPermeability: float

    Young: float
    Poisson: float
    CoefDilatation: float
    
    ref: Optional[str] = None

##################
#
##################

class MPartMagnetLink(SQLModel, table=True):
    """
    MPart/Magnet many to many link table
    """
    magnet_id: Optional[int] = Field(
        default=None, foreign_key="magnet.id", primary_key=True
    )
    mpart_id: Optional[int] = Field(
        default=None, foreign_key="mpart.id", primary_key=True
    )

class MagnetMSiteLink(SQLModel, table=True):
    """
    Magnet/Site many to many link table
    """
    magnet_id: Optional[int] = Field(
        default=None, foreign_key="magnet.id", primary_key=True
    )
    msite_id: Optional[int] = Field(
        default=None, foreign_key="msite.id", primary_key=True
    )

##################
#
##################

class MSiteBase(SQLModel):
    """
    Magnet Site
    """
    name: str
    conffile: str
    status: str

class MSite(MSiteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    magnets: List["Magnet"] = Relationship(back_populates="msites", link_model=MagnetMSiteLink)

class MSiteRead(MSiteBase):
    id: int

class MSiteCreate(MSiteBase):
    pass

class MSiteUpdate(SQLModel):
    """
    Magnet Site
    """
    name: str
    conffile: str
    status: str
    magnets: List["Magnet"] = [] # Relationship(back_populates="msites", link_model=MagnetMSiteLink)

##################
#
##################

class MagnetBase(SQLModel):
    """
    Magnet
    """
    name: str

    be: str
    geom: str
    status: str


class Magnet(MagnetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    msites: List[MSite] = Relationship(back_populates="magnets", link_model=MagnetMSiteLink)
    mparts: List["MPart"] = Relationship(back_populates="magnets", link_model=MPartMagnetLink)

class MagnetRead(MagnetBase):
    id: int

class MagnetCreate(MagnetBase):
    pass

class MagnetUpdate(SQLModel):
    """
    Magnet
    """
    name: str

    be: str
    geom: str
    status: str

    msites: List[MSite] = [] #Relationship(back_populates="magnets", link_model=MagnetMSiteLink)
    mparts: List["MPart"] = [] #Relationship(back_populates="magnets", link_model=MPartMagnetLink)

##################
#
##################

class MPartBase(SQLModel):
    """
    Magnet Part
    """
    name: str

    type: str
    be: str
    geom: str
    status: str

    material_id: Optional[int] = Field(default=None, foreign_key="material.id")

class MPart(MPartBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # material: Optional[Material] = Relationship(back_populates="mparts")
    magnets: List[Magnet] = Relationship(back_populates="mparts", link_model=MPartMagnetLink)

class MPartRead(MPartBase):
    id: int

class MPartCreate(MPartBase):
    pass

class MPartUpdate(SQLModel):
    """
    Magnet Part
    """
    name: str

    type: str
    be: str
    geom: str
    status: str

    material_id: Optional[int] = None
    magnets: List[Magnet] = []

##################
#
##################

"""
class MPartReadWithMaterial(MPartRead):
    material: Optional[MaterialRead]
"""

class MPartReadWithMagnet(MPartRead):
    magnets: List[MagnetRead] = []

class MagnetReadWithMParts(MagnetRead):
    mparts: List[MPartRead] = []

class MagnetReadWithMSite(MagnetRead):
    msites: List[MSiteRead] = []

class MSiteReadWithMagnets(MSiteRead):
    magnets: List[MagnetRead] = []


##################
#
##################

class MRecordBase(SQLModel):
    """
    Magnet Record
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: str
    name: str
    msite_id: Optional[int] = Field(default=None, foreign_key="msite.id")

class MRecord(MRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # msite: Optional[MSite] = Relationship(back_populates="msites")

class MRecordRead(MRecordBase):
    id: int

class MRecordCreate(MRecordBase):
    pass

class MRecordUpdate(SQLModel):
    """
    Magnet Record
    """
    timestamp: str
    name: str
    msite_id: Optional[int] = None #Field(default=None, foreign_key="msite.id")
