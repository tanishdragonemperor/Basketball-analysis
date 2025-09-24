import {
  ChangeDetectorRef,
  Component,
  OnDestroy,
  OnInit,
  ViewEncapsulation
} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {untilDestroyed, UntilDestroy} from '@ngneat/until-destroy';
import {PlayersService} from '../_services/players.service';
import {PlayerSummary, ActionTypeStats} from '../models/player-summary.interface';

@UntilDestroy()
@Component({
  selector: 'player-summary-component',
  templateUrl: './player-summary.component.html',
  styleUrls: ['./player-summary.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class PlayerSummaryComponent implements OnInit, OnDestroy {
  
  playerSummary: PlayerSummary | null = null;
  loading = false;
  error: string | null = null;
  selectedActionType: string = 'pickAndRoll';
  selectedPlayerId: number = 0;

  actionTypes = [
    { key: 'pickAndRoll', label: 'Pick & Roll', color: '#3f51b5' },
    { key: 'isolation', label: 'Isolation', color: '#f44336' },
    { key: 'postUp', label: 'Post-up', color: '#4caf50' },
    { key: 'offBallScreen', label: 'Off-Ball Screen', color: '#ff9800' }
  ];

  constructor(
    protected activatedRoute: ActivatedRoute,
    protected cdr: ChangeDetectorRef,
    protected playersService: PlayersService,
  ) {
  }

  ngOnInit(): void {
    // Get player ID from route params or default to 0
    this.activatedRoute.params.pipe(untilDestroyed(this)).subscribe(params => {
      this.selectedPlayerId = params['playerId'] ? parseInt(params['playerId']) : 0;
      this.loadPlayerSummary();
    });
  }

  loadPlayerSummary(): void {
    this.loading = true;
    this.error = null;
    
    this.playersService.getPlayerSummary(this.selectedPlayerId)
      .pipe(untilDestroyed(this))
      .subscribe({
        next: (data) => {
          this.playerSummary = data.apiResponse;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (error) => {
          this.error = 'Failed to load player data. Please try again.';
          this.loading = false;
          this.cdr.detectChanges();
        }
      });
  }

  onPlayerIdChange(): void {
    if (this.selectedPlayerId >= 0 && this.selectedPlayerId <= 9) {
      this.loadPlayerSummary();
    }
  }

  getActionTypeStats(): ActionTypeStats | null {
    if (!this.playerSummary) return null;
    return this.playerSummary[this.selectedActionType as keyof PlayerSummary] as ActionTypeStats;
  }

  getActionCount(): number {
    if (!this.playerSummary) return 0;
    const countKey = this.selectedActionType + 'Count' as keyof PlayerSummary;
    return this.playerSummary[countKey] as number;
  }

  getSelectedActionTypeLabel(): string {
    const actionType = this.actionTypes.find(a => a.key === this.selectedActionType);
    return actionType ? actionType.label : '';
  }

  getSelectedActionTypeColor(): string {
    const actionType = this.actionTypes.find(a => a.key === this.selectedActionType);
    return actionType ? actionType.color : '#666';
  }

  getCourtX(x: number): number {
    // Convert court coordinates to pixel positions
    // Court is 50 feet wide, so scale to fit the container
    // Center the court horizontally
    const courtWidth = 50; // feet
    const containerWidth = 800; // pixels (max-width from CSS)
    const scale = containerWidth / courtWidth;
    return (x + 25) * scale; // +25 to center (court goes from -25 to +25)
  }

  getCourtY(y: number): number {
    // Convert court coordinates to pixel positions
    // Court is 47 feet long (full court), so scale to fit the container
    // Center the court vertically
    const courtLength = 47; // feet
    const containerHeight = 500; // pixels (height from CSS)
    const scale = containerHeight / courtLength;
    return (y + 23.5) * scale; // +23.5 to center (court goes from -23.5 to +23.5)
  }

  getRankText(rank: number | undefined): string {
    if (!rank) return 'N/A';
    const suffixes = ['th', 'st', 'nd', 'rd'];
    const v = rank % 100;
    return rank + (suffixes[(v - 20) % 10] || suffixes[v] || suffixes[0]);
  }

  getRankColor(rank: number | undefined): string {
    if (!rank) return '#666';
    if (rank <= 3) return '#4caf50'; // Green for top 3
    if (rank <= 6) return '#ff9800'; // Orange for middle
    return '#f44336'; // Red for bottom
  }

  ngOnDestroy() {
  }
}