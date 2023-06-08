USE [TEST_API]
GO

/****** Object:  Table [dbo].[TaxiAvailability]    Script Date: 8/6/2023 10:18:21 AM ******/
/****** Table is storing taxi availability data from https://data.gov.sg/dataset/taxi-availability ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[TaxiAvailability](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[Timestamp] [datetime] NULL,
	[Location] [geometry] NULL,
	[TaxiCount] [int] NULL,
	[RegionID] [int] NULL,
	[RegionDetectedFlag] [tinyint] NULL,
PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[TaxiAvailability]  WITH CHECK ADD  CONSTRAINT [FK_RegionID] FOREIGN KEY([RegionID])
REFERENCES [dbo].[RegionBoundaries] ([ID])
GO

ALTER TABLE [dbo].[TaxiAvailability] CHECK CONSTRAINT [FK_RegionID]
GO





/****** Object:  Table [dbo].[RegionBoundaries]    Script Date: 8/6/2023 10:18:47 AM ******/
/****** Table is storing subzone boundaries data from https://data.gov.sg/dataset/master-plan-2019-subzone-boundary-no-sea?resource_id=84b62d90-c1b7-4ada-acfc-f5874b5fd945 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[RegionBoundaries](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[RegionName] [varchar](100) NULL,
	[RegionCode] [varchar](10) NULL,
	[Geometry] [geometry] NULL,
	[SubZoneNo] [varchar](20) NULL,
	[SubZoneName] [varchar](200) NULL,
	[SubZoneCode] [varchar](200) NULL,
	[AreaName] [varchar](200) NULL,
	[AreaCode] [varchar](200) NULL,
	[INC_CRC] [varchar](60) NULL,
	[FMEL_UPD_D] [varchar](60) NULL,
 CONSTRAINT [PK__RegionBo__3214EC271A60D00C] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO


