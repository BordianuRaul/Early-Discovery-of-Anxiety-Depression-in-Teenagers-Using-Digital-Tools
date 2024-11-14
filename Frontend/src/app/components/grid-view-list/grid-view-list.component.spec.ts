import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GridViewListComponent } from './grid-view-list.component';

describe('GridViewListComponent', () => {
  let component: GridViewListComponent;
  let fixture: ComponentFixture<GridViewListComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GridViewListComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GridViewListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
